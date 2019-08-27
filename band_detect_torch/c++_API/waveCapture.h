#pragma once
#include <iostream>
#include <fstream>
#include <string>
#include <vector>

#ifdef _DEBUG
#define PRINT   printf
#else
#define PRINT(...)
#endif

namespace std {
	struct band
	{
		char  sWaveID[36];       //载波ID
		double freq_mid;          //载波中心频点,单位MHz
		double band_width;               //载波带宽,单位MHz
		float amptitude;      //信号电平,单位dBm
		float cnr;               //载噪比,单位dB
		char waveFitting;
	};

	class WaveCapture {
	public:
		WaveCapture() {};
		WaveCapture(string filePath);
		~WaveCapture() {
			sigStream.close();
			frame_pos.clear();
			result.clear();
			//delete data_ave;
			//delete data_max;
		};

		void data_update();
		void read_frame(size_t frame_num);
		void scan_frame();

		vector<float> get_data_ave();
		vector<float> get_data_max();
		vector<band> get_wave_result();

		vector<float> get_data_ave(size_t frame);
		vector<float> get_data_max(size_t frame);
		vector<band> get_wave_result(size_t frame);

		double wave_freq_start() {
			return freq_start;
		}
		double wave_freq_end() {
			return freq_end;
		}
		double wave_freq_res() {
			freq_res = (freq_end - freq_start) / (fft_len / 2);
			return freq_res;
		}

		void data_update(string file_path) {
			filePath = file_path;
			data_update();
		}

	private:
		// 文件信息
		string filePath;  // 文件名路径 
		std::ifstream sigStream;  // 文件读入流

		// 输出文件帧头判断
		bool is_output;
		size_t version_len = 16;
		const string output_head = "wavemark 1.0";

		// 信号流控制参数
		vector<ifstream::pos_type> frame_pos;  // 所有帧起始流位置
		ifstream::pos_type end_pos = 0;  // 文件流总长
		size_t cur_sig_frame = 0;  // 当前帧数
		size_t all_sig_frame = 0;  // 总帧数

		// 帧头参数
		int syn_code;  // 同步码
		char ver;  // 版本号
		double freq_start;  // 起始频率
		double freq_end;  // 结束频率
		double freq_res;  // 频谱分辨率
		char spec_type;  // 频谱数据类型
		int spec_bit;  // 频谱数据位数

		// 频谱数据
		int fft_len;  // 频谱数据总长度
		vector<float> fft_data;  // 频谱数据
		//float *data_ave;
		//float *data_max;
		
		int single_band_len;  // 单个检测结果长度：60
		int band_res_nums;  // 载波检测结果个数
		vector<band> result;  // 当前帧载波检测结果

	};

} //namespace std;