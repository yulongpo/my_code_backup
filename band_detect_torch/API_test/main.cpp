#include <iostream>
#include "waveCapture.h"
#include "CarrierDetect.h"
#include <direct.h>

#include <Windows.h>  // ��ʱ

const unsigned MAX_RESULT_LEN = 256;

void create_InSpecDataParam(InSpecDataParam &sInParam, std::WaveCapture &wave_c) {
	sInParam.dTaskStartFreq = wave_c.wave_freq_start()/1e6;
	sInParam.dTaskEndFreq = wave_c.wave_freq_end()/1e6;
	sInParam.dFreqReso = wave_c.wave_freq_res()/1e6;
	sInParam.dCNThreshold = 4;
	sInParam.dBwThreshold = sInParam.dFreqReso * 8;
}

std::string get_cur_dir() {
	if (_getcwd(NULL, 0) == NULL)
	{
		perror("getcwd error");
		return std::string();
	}
	else
	{
		return std::string(_getcwd(NULL, 0));
	}
}

int main(int argc, const char* argv[]) {
	std::string file_name = get_cur_dir() + "\\FFT_2018_08_11_12_570425365_GSat14-V-4680_2";

	if (argc > 1) {
		file_name = std::string(argv[1]);
	}
	
	std::WaveCapture wave_capture(file_name);


	auto *p = CreateCCarrierDetectClass();
	InSpecDataParam sInParam;
	create_InSpecDataParam(sInParam, wave_capture);

	std::vector<float> data_v = wave_capture.get_data_max();

	std::cout << data_v.size() * sInParam.dFreqReso << "\n";
	//data_v = std::vector<float>(data_v.begin(), data_v.begin() + 16384);
	sInParam.dTaskEndFreq = data_v.size() * sInParam.dFreqReso + sInParam.dTaskStartFreq;

	char *intData = (char *)malloc(data_v.size() * sizeof(char));
	for (int i = 0; i != data_v.size(); ++i) {
		intData[i] = char(data_v[i]);
	}
	SP_Signal *sResult = (SP_Signal*)malloc(MAX_RESULT_LEN*sizeof(SP_Signal));
	int m_nSigNum;

	double stop_fres;

	//printf("��ʱ��ʼ---------------------\n");
	///**************************************************************************/
	//double run_time;
	//_LARGE_INTEGER time_start;	//��ʼʱ��
	//_LARGE_INTEGER time_over;	//����ʱ��
	//double dqFreq;		//��ʱ��Ƶ��
	//LARGE_INTEGER f;	//��ʱ��Ƶ��
	//QueryPerformanceFrequency(&f);
	//dqFreq = (double)f.QuadPart;
	//QueryPerformanceCounter(&time_start);	//��ʱ��ʼ

	////Ҫ��ʱ�ĳ���
	//CarrierDetectAndCheckValidFreqProInterface(p, intData, data_v.size(), sInParam, sResult, m_nSigNum, stop_fres);


	//QueryPerformanceCounter(&time_over);	//��ʱ����
	//run_time = 1000000 * (time_over.QuadPart - time_start.QuadPart) / dqFreq;
	////����1000000�ѵ�λ���뻯Ϊ΢�룬����Ϊ1000 000/��cpu��Ƶ��΢��
	//printf("\nrun_time��%fus\n", run_time);
	///**************************************************************************/
	//printf("��ʱ����---------------------\n");

	for (int i = 0; i < 10; ++i) {
		printf("��%03d��\n", i);
		CarrierDetectAndCheckValidFreqProInterface(p, intData, data_v.size(), sInParam, sResult, m_nSigNum, stop_fres);
	}


	//CarrierDetectProInterface(p, intData, data_v.size(), sInParam, sResult, m_nSigNum);
	//CarrierDetectAndCheckValidFreqProInterface(p, intData, data_v.size(), sInParam, sResult, m_nSigNum, stop_fres);
	for (int i = 0; i != m_nSigNum; ++i) {
		SP_Signal band = sResult[i];
		printf("%3d:\tmid_freq=%.3f MHz\tband_width=%.3f MHz\tCNR=%.3f dB\tAmptitude=%.3f dB\n",
			i + 1, band.dFreqMid, band.dBW, band.dCN, band.dSignalLevel);
	}

	printf("��Ч��ֹƵ�ʣ�%.3f\n", stop_fres);
	printf("��Ƶ�ʣ�%.3f\n", sInParam.dFreqReso*data_v.size() + sInParam.dTaskStartFreq);


	DeleteCCarrierDetectClass(p);
	delete intData;
	delete sResult;

	system("pause");

	return 0;
}