#include "waveCapture.h"

namespace std {
	std::WaveCapture::WaveCapture(string filePath) :
		filePath(filePath)
	{
		data_update();
	}

	void std::WaveCapture::data_update()
	{
		sigStream.close();
		sigStream.open(filePath, std::ios::binary);
		if (!sigStream) {
			PRINT("STREAM NOT OK!\n"); // std::cout << "STREAM NOT OK!" << std::endl;
			all_sig_frame = 0;
			return;
		}
		PRINT("STREAM OK!\n"); // std::cout << "STREAM OK!" << std::endl;

		frame_pos.clear();
		result.clear();

		sigStream.seekg(0, SEEK_END);
		end_pos = sigStream.tellg();
		sigStream.seekg(0);

		char tmp_ver[16];
		sigStream.read(reinterpret_cast<char*>(tmp_ver), sizeof(tmp_ver));
		if (string(tmp_ver) == output_head) {
			is_output = true;
		}
		else {
			is_output = false;
			sigStream.seekg(0);
		}

		while (sigStream.tellg() < end_pos) {
			frame_pos.push_back(sigStream.tellg());
			scan_frame();
		}

		all_sig_frame = frame_pos.size();
		if (all_sig_frame) {
			cur_sig_frame = 1;
			read_frame(cur_sig_frame);
		}

	}

	void std::WaveCapture::read_frame(size_t frame_num)
	{
		if (frame_num < 0 || frame_num > all_sig_frame) {
			printf("错误指定帧数：%d, 当前文件最大帧数：%d", frame_num, all_sig_frame);
			return;
		}
			
		cur_sig_frame = frame_num;
		sigStream.seekg(frame_pos[cur_sig_frame - 1]);

		sigStream.read(reinterpret_cast<char*>(&syn_code), sizeof(syn_code));
		sigStream.read(reinterpret_cast<char*>(&ver), sizeof(ver));
		sigStream.read(reinterpret_cast<char*>(&freq_start), sizeof(freq_start));
		sigStream.read(reinterpret_cast<char*>(&freq_end), sizeof(freq_end));
		sigStream.read(reinterpret_cast<char*>(&freq_res), sizeof(freq_res));
		sigStream.read(reinterpret_cast<char*>(&spec_type), sizeof(spec_type));

		sigStream.read(reinterpret_cast<char*>(&fft_len), sizeof(fft_len));
		char* tmp_data = new char[fft_len];
		sigStream.read(reinterpret_cast<char*>(tmp_data), fft_len * sizeof(char));
		fft_data = vector<float>(tmp_data, tmp_data + fft_len);
		delete tmp_data;

		//data_ave = new float[sizeof(float) * fft_len / 2];
		//data_max = new float[sizeof(float) * fft_len / 2];

		//auto tmp_ave = vector<float>(fft_data.begin(), fft_data.begin() + fft_len / 2);
		//data_ave = tmp_ave.data();
		//data_max = vector<float>(fft_data.end() - fft_len / 2, fft_data.end()).data();

		sigStream.read(reinterpret_cast<char*>(&single_band_len), sizeof(single_band_len));
		sigStream.read(reinterpret_cast<char*>(&band_res_nums), sizeof(band_res_nums));
		result.clear();
		for (int i = 0; i < band_res_nums; ++i) {
			band tmp_band;
			sigStream.read(reinterpret_cast<char*>(tmp_band.sWaveID), sizeof(tmp_band.sWaveID));
			sigStream.read(reinterpret_cast<char*>(&tmp_band.freq_mid), sizeof(tmp_band.freq_mid));
			sigStream.read(reinterpret_cast<char*>(&tmp_band.band_width), sizeof(tmp_band.band_width));
			sigStream.read(reinterpret_cast<char*>(&tmp_band.amptitude), sizeof(tmp_band.amptitude));
			sigStream.read(reinterpret_cast<char*>(&tmp_band.cnr), sizeof(tmp_band.cnr));

			if (is_output)
				sigStream.read(reinterpret_cast<char*>(&tmp_band.waveFitting), sizeof(tmp_band.waveFitting));

			result.push_back(tmp_band);
		}
		
	}

	void std::WaveCapture::scan_frame()
	{
		// 跳过帧头的数据
		sigStream.seekg(30, std::ios::cur);

		// 获取帧数据长度，并跳过帧数据
		int arraySize = 0;
		sigStream.read(reinterpret_cast<char*>(&arraySize), sizeof(arraySize));
		sigStream.seekg(arraySize, std::ios::cur);

		// 获取载波数据长度，并跳过载波数据
		int waveLen = 0, waveCnt = 0;
		sigStream.read(reinterpret_cast<char*>(&waveLen), sizeof(waveLen));
		sigStream.read(reinterpret_cast<char*>(&waveCnt), sizeof(waveCnt));
		sigStream.seekg(waveLen * waveCnt, std::ios::cur);
	}

	vector<float> std::WaveCapture::get_data_ave()
	{
		return vector<float>(fft_data.begin(), fft_data.begin() + fft_len / 2);
	}

	vector<float> std::WaveCapture::get_data_max()
	{
		return vector<float>(fft_data.end() - fft_len / 2, fft_data.end());
	}

	vector<band> std::WaveCapture::get_wave_result()
	{
		return result;
	}

	vector<float> std::WaveCapture::get_data_ave(size_t frame)
	{
		if (cur_sig_frame != frame)
			read_frame(frame);
		return get_data_ave();
	}

	vector<float> std::WaveCapture::get_data_max(size_t frame)
	{
		if (cur_sig_frame != frame)
			read_frame(frame);
		return get_data_max();
	}

	vector<band> std::WaveCapture::get_wave_result(size_t frame)
	{
		if (cur_sig_frame != frame)
			read_frame(frame);
		return get_wave_result();
	}
}