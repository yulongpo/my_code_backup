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
		char  sWaveID[36];       //�ز�ID
		double freq_mid;          //�ز�����Ƶ��,��λMHz
		double band_width;               //�ز�����,��λMHz
		float amptitude;      //�źŵ�ƽ,��λdBm
		float cnr;               //�����,��λdB
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
		// �ļ���Ϣ
		string filePath;  // �ļ���·�� 
		std::ifstream sigStream;  // �ļ�������

		// ����ļ�֡ͷ�ж�
		bool is_output;
		size_t version_len = 16;
		const string output_head = "wavemark 1.0";

		// �ź������Ʋ���
		vector<ifstream::pos_type> frame_pos;  // ����֡��ʼ��λ��
		ifstream::pos_type end_pos = 0;  // �ļ����ܳ�
		size_t cur_sig_frame = 0;  // ��ǰ֡��
		size_t all_sig_frame = 0;  // ��֡��

		// ֡ͷ����
		int syn_code;  // ͬ����
		char ver;  // �汾��
		double freq_start;  // ��ʼƵ��
		double freq_end;  // ����Ƶ��
		double freq_res;  // Ƶ�׷ֱ���
		char spec_type;  // Ƶ����������
		int spec_bit;  // Ƶ������λ��

		// Ƶ������
		int fft_len;  // Ƶ�������ܳ���
		vector<float> fft_data;  // Ƶ������
		//float *data_ave;
		//float *data_max;
		
		int single_band_len;  // ������������ȣ�60
		int band_res_nums;  // �ز����������
		vector<band> result;  // ��ǰ֡�ز������

	};

} //namespace std;