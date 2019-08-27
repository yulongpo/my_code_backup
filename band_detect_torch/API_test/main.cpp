#include <iostream>
#include "waveCapture.h"
#include "CarrierDetect.h"
#include <direct.h>

#include <Windows.h>  // 计时

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

	//printf("计时开始---------------------\n");
	///**************************************************************************/
	//double run_time;
	//_LARGE_INTEGER time_start;	//开始时间
	//_LARGE_INTEGER time_over;	//结束时间
	//double dqFreq;		//计时器频率
	//LARGE_INTEGER f;	//计时器频率
	//QueryPerformanceFrequency(&f);
	//dqFreq = (double)f.QuadPart;
	//QueryPerformanceCounter(&time_start);	//计时开始

	////要计时的程序
	//CarrierDetectAndCheckValidFreqProInterface(p, intData, data_v.size(), sInParam, sResult, m_nSigNum, stop_fres);


	//QueryPerformanceCounter(&time_over);	//计时结束
	//run_time = 1000000 * (time_over.QuadPart - time_start.QuadPart) / dqFreq;
	////乘以1000000把单位由秒化为微秒，精度为1000 000/（cpu主频）微秒
	//printf("\nrun_time：%fus\n", run_time);
	///**************************************************************************/
	//printf("计时结束---------------------\n");

	for (int i = 0; i < 10; ++i) {
		printf("第%03d次\n", i);
		CarrierDetectAndCheckValidFreqProInterface(p, intData, data_v.size(), sInParam, sResult, m_nSigNum, stop_fres);
	}


	//CarrierDetectProInterface(p, intData, data_v.size(), sInParam, sResult, m_nSigNum);
	//CarrierDetectAndCheckValidFreqProInterface(p, intData, data_v.size(), sInParam, sResult, m_nSigNum, stop_fres);
	for (int i = 0; i != m_nSigNum; ++i) {
		SP_Signal band = sResult[i];
		printf("%3d:\tmid_freq=%.3f MHz\tband_width=%.3f MHz\tCNR=%.3f dB\tAmptitude=%.3f dB\n",
			i + 1, band.dFreqMid, band.dBW, band.dCN, band.dSignalLevel);
	}

	printf("有效截止频率：%.3f\n", stop_fres);
	printf("总频率：%.3f\n", sInParam.dFreqReso*data_v.size() + sInParam.dTaskStartFreq);


	DeleteCCarrierDetectClass(p);
	delete intData;
	delete sResult;

	system("pause");

	return 0;
}