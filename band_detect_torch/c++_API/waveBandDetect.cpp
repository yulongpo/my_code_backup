#include "WaveBandDetect.h"

bool WaveBandDetct::load_model()
{
	try {
		// Deserialize the ScriptModule from a file using torch::jit::load().
		model = torch::jit::load(model_path);
	}
	catch (const c10::Error& e) {
		std::cerr << "error loading the model: " << model_path << "\n";
		return false;
	}

	//model = torch::jit::load(model_path);
	//if (model == nullptr)  // 判断模型是否加载成功
	//	return false;

	model->to(DVICE);  // 如有GPU使用GPU
	model->eval();

	// 更新缓存数据
	data_origin.clear();
	inputs.clear();
	data_origin_start = -1;
	pred_wave_bands.clear();

	return true;
}

void WaveBandDetct::wave_detect()
{
	if (data_origin.empty())
		return;
	data_preprocessing();
	tmp_pred = model->forward(inputs).toTensor().to(at::kCPU).view(-1);
	tmp_pred = torch::where(tmp_pred > 0.5, torch::ones(tmp_pred.size(0)), torch::zeros(tmp_pred.size(0)));
	result_smooth(tmp_pred);
}

void WaveBandDetct::data_preprocessing()
{
	torch::Tensor data = data_origin_tensor;
	//std::cout << data.slice(0, 0, 40) << std::endl;
	data = (data - data.min()) / (data.max() - data.min());
	auto tmp_d1 = data.slice(0, 1) - data.slice(0, 0, data.size(0) - 1);

	tmp_d1 += (torch::abs(tmp_d1) - tmp_d1) / 2;
	auto d1 = torch::empty(data.size(0));
	d1[0] = tmp_d1[0];
	d1.slice(0, 1) = tmp_d1;
	//std::cout << d1.slice(0, 0, 40) << std::endl;
	data -= d1;

	auto _threshold = (data.max().item<float>() - data.min().item<float>()) / 22;

	int h = int(data.std().item<float>() * 200);

	// 正向求start
	auto tmp = torch::zeros(h + data.size(0) - 1);
	tmp.slice(0, 0, data.size(0)) = data;
	tmp.slice(0, data.size(0)) += data[-1];

	auto ave = torch::avg_pool1d(tmp.view({ 1, 1, -1 }), h, 1).flatten();

	tmp = data - ave + _threshold;

	int start = 0;
	for (int i = 0; i < tmp.size(0); ++i) {
		if (tmp[i].item<float>() < 0) {
			start = i;
			break;
		}
	}

	// 反向求end
	tmp = torch::zeros(h + data.size(0) - 1);
	for (int i = 0; i < data.size(0); ++i) {
		tmp[i] = data[data.size(0) - i - 1];
	}
	tmp.slice(0, data.size(0)) += data[0];
	ave = torch::avg_pool1d(tmp.view({ 1, 1, -1 }), h, 1).flatten();
	//std::cout << ave.sizes() << "\n"
	//	<< ave.slice(0, 0, 40) << std::endl;

	tmp = tmp.slice(0, 0, data.size(0)) - ave + _threshold;
	//std::cout << tmp.slice(0, 0, 40) << std::endl;

	int end = 0;
	for (int i = 0; i < tmp.size(0); i++) {
		if (tmp[i].item<float>() < 0) {
			end = i;
			break;
		}

	}
	end = data.size(0) - end;

	data = data_origin_tensor.slice(0, start, end);
	data = (data - data.min()) / (data.max() - data.min());

	// 
	data_origin_start = start;
	inputs.push_back(data.view({ 1, 1, -1 }).to(DVICE));
}

void WaveBandDetct::result_smooth(torch::Tensor _pred)
{
	auto pred = _pred;
	if (pred[0].item<float>() > 0) {
		auto tmp = torch::empty(pred.size(0) + 1);
		tmp[0] = 0;
		tmp.slice(0, 1) = pred;
		pred = tmp;
	}
	if (pred[-1].item<float>() > 0) {
		auto tmp = torch::empty(pred.size(0) + 1);
		tmp[-1] = 0;
		tmp.slice(0, 0, pred.size(0)) = pred;
		pred = tmp;
	}

	auto y = pred.slice(0, 0, pred.size(0) - 1) - pred.slice(0, 1);

	std::vector<int> label_start, label_end;
	float item = 0;
	for (int i = 0; i < y.size(0); ++i) {
		item = y[i].item<float>();
		if (item < 0) {
			label_start.push_back(i + data_origin_start);
		}
		else if (item > 0) {
			label_end.push_back(i + data_origin_start);
		}
	}

	assert(label_start.size() == label_end.size());

	//std::vector<band_info> true_labels;
	band_info tmp_label;
	float left_min = 0., right_min = 0.;

	for (int i = 0; i < label_start.size(); ++i) {
		if (label_end[i] - label_start[i] < least_band_width)
			continue;

		tmp_label = band_info();
		left_min = 0.;
		right_min = 0.;

		tmp_label.x = label_start[i];
		tmp_label.y = label_end[i];
		int w = tmp_label.y - tmp_label.x;  // label's points width
		int smooth_len = int(round(w / 7));

		tmp_label.amptitude = data_origin_tensor.slice(0,
			tmp_label.x + smooth_len,
			tmp_label.y - smooth_len).mean().item<float>();

		calculate_min(w, left_min, right_min, tmp_label);
		
		if (tmp_label.cnr > cnr_threshold) {
			pred_wave_bands.push_back(tmp_label);
		}
	}

}

void WaveBandDetct::calculate_min(int w, float & left_min, float & right_min, band_info & tmp_label)
{
	int min_w = int(w * 0.2);
	if (tmp_label.x - min_w < 0) {
		left_min = data_origin_tensor.slice(0, 0, tmp_label.x + 1).min().item<float>();
	}
	else {
		left_min = data_origin_tensor.slice(0, tmp_label.x - min_w, tmp_label.x + 1).min().item<float>();
	}
	if (tmp_label.y + min_w > data_origin_tensor.size(0) + 1) {
		right_min = data_origin_tensor.slice(0, tmp_label.y - 1).min().item<float>();
	}
	else {
		right_min = data_origin_tensor.slice(0, tmp_label.y - 1, tmp_label.y + min_w).min().item<float>();
	}

	tmp_label.cnr = tmp_label.amptitude - (left_min < right_min ? left_min : right_min);
}

//void WaveBandDetct::compute_band_info()
//{
//}
