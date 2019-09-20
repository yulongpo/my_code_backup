#pragma once

#include <torch/script.h> // One-stop header.
#include <torch/cuda.h>

#include <iostream>
#include <memory>
#include <string>
#include <cmath>

struct band_info
{
	int x;
	int y;
	float amptitude;      //信号电平,单位dBm
	float cnr;               //载噪比,单位dB
};

class WaveBandDetct {
public:
	WaveBandDetct() = default;
	WaveBandDetct(const std::string model_path) :model_path(model_path)
	{
		if (!load_model()) {
			std::cout << "权重模型加载错误！" << std::endl;
		}
	}
	~WaveBandDetct() {}

	void calculate_min(int w, float &left_min, float &right_min, band_info &tmp_label);

	std::vector<band_info> detect() {
		pred_wave_bands.clear();
		inputs.clear();
		wave_detect();
		return pred_wave_bands;
	}
	std::vector<band_info> detect(const std::vector<float> data) {
		set_data(data);
		return detect();
	}
	std::vector<band_info> detect(const char* data, char nMeanOrMax, const int len) { // nMeanOrMax: 平均谱（0）或最大谱（1）
		set_data(data, nMeanOrMax, len);
		return detect();
	}

	bool load_model(const std::string model_path) {
		this->model_path = model_path;
		return load_model();
	}

	void set_data(const std::vector<float> data) {
		data_origin = data;
		data_origin_tensor = torch::from_blob(data_origin.data(), (data_origin.size()));
	}

	template <typename T>
	void set_data(const T* data, char nMeanOrMax, const int all_data_len) { // nMeanOrMax: 平均谱（0）或最大谱（1）
		if (nMeanOrMax == 0) {
			data_origin = std::vector<float>(data, data + all_data_len /2);
		}
		else if (nMeanOrMax == 1) {
			data_origin = std::vector<float>(data + all_data_len / 2, data + all_data_len);
		}
		data_origin_tensor = torch::from_blob(data_origin.data(), (data_origin.size()));
	}

	// 设置载噪比门限
	void set_cnr_threshold(const double thr) {
		cnr_threshold = thr;
	}

	// 设置最小带宽门限
	// @dBwThreshold： 门限带宽MHz
	// @freq_res: 当前频谱数据分辨率
	void set_least_band_width(const double dBwThreshold, const double freq_res) {
		least_band_width = int(round(dBwThreshold / freq_res));
	}

private:
	// 模型权重文件路径
	std::string model_path;
	// torch模型
	std::shared_ptr<torch::jit::script::Module> model;

	// GPU or CPU
	const c10::DeviceType DVICE = torch::cuda::is_available() ? torch::kCUDA : torch::kCPU;

	// 原始频谱数据
	std::vector<float> data_origin;
	torch::Tensor data_origin_tensor;

	int data_origin_start = 0;
	std::vector<torch::jit::IValue> inputs;
	std::vector<band_info> pred_wave_bands;
	double cnr_threshold = 4.5;
	int least_band_width = 7;

	torch::Tensor tmp_pred;

	bool load_model();
	void wave_detect();
	void data_preprocessing();
	void result_smooth(torch::Tensor _pred);
	//void compute_band_info();

};