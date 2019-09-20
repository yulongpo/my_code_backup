#include "CarrierDetect.h"
#include "WaveBandDetect.h"
#include <direct.h>

#include <algorithm>
#include <iterator>

#include <fstream>

#include "myLog.hpp"

#include <map>
#include <fstream>

#define config_path "./config/CarrierDetectDLL.ini"


class Detect_and_Logger {
public:
	Detect_and_Logger() = default;
	Detect_and_Logger(std::string model_path, std::string log_file_path, bool create_log=false)
		: model_path(model_path), log_file_path(log_file_path)
	{
		try {
			loger_p = new MyLogging(log_file_path, create_log);
		}
		catch (const std::bad_alloc ex) {
			std::cerr << "��־�������ڴ�������:" << ex.what() << std::endl;
		}

		try {
			detect_p = new WaveBandDetct(model_path);
		}
		catch (const std::bad_alloc ex) {
			std::cerr << "�ز�������ڴ�������:" << ex.what() << std::endl;
		}
	}

	WaveBandDetct *detect_p;
	MyLogging *loger_p;

private:
	std::string model_path;
	std::string log_file_path;
};

void ConfigFileRead(std::map<std::string, std::string>& m_mapConfigInfo)
{
	spdlog::set_level(spdlog::level::trace);

	std::ifstream configFile;
	std::string path = std::string(config_path);
	configFile.open(path.c_str());
	std::string str_line;
	if (configFile.is_open())
	{
		while (!configFile.eof())
		{
			std::getline(configFile, str_line);

			//���˵����С�ע����Ϣ
			if (str_line.size() == 0 || str_line.find('#') == 0)
			{
				continue;
			}
			if (str_line.find('[') == 0) {
				spdlog::debug(str_line);
				continue;
			}
			spdlog::debug(str_line);
			size_t pos = str_line.find('=');
			std::string str_key = str_line.substr(0, pos);
			std::string str_value = str_line.substr(pos + 1);
			m_mapConfigInfo.insert(std::pair<std::string, std::string>(str_key, str_value));
		}
	}
	else
	{
		std::cerr << "Cannot open config file path: " << path << std::endl;;
		exit(-1);
	}
	configFile.close();
}

std::string findValueFromMap(std::map<std::string, std::string> mapConfigInfo, std::string aimValue) {
	std::map<std::string, std::string>::iterator iter_configMap;
	iter_configMap = mapConfigInfo.find(aimValue);
	if (iter_configMap == mapConfigInfo.end()) {
		std::cerr << "Error: " << aimValue << " not being defined in config file!" << std::endl;
		exit(-1);
	}
	else {
		return iter_configMap->second;
	}
}

// ����Ĭ����־��
std::string createDefaultLogFile() {
	std::string folderPath = "logs";
	if (0 != _access(folderPath.c_str(), 0))
	{
		// if this folder not exist, create a new one.
		_mkdir(folderPath.c_str());   // ���� 0 ��ʾ�����ɹ���-1 ��ʾʧ��
	}

	std::time_t t = std::time(NULL);
	char log_file_name[100];
	std::strftime(log_file_name, sizeof(log_file_name), "logs/Log_%y-%m-%e_CarrierDetectDLL.txt", std::localtime(&t));
	spdlog::debug("log_file_path: {}", log_file_name);

	return std::string(log_file_name);
}

// ��ȡĬ��Ȩ��·��
std::string getDefaultModelPath() {
	char *buffer;
	std::string model_path;
	//Ҳ���Խ�buffer��Ϊ�������
	if ((buffer = _getcwd(NULL, 0)) == NULL)
	{
		perror("�޷�����ģ�ͣ���ȡ��ǰ��ַ����");
	}
	else
	{
		model_path = std::string(buffer);
		delete buffer;
	}

	model_path += "\\band_detect_torch.pt";
	return model_path;
}

int checkoutInputArgs(int nIntLen, InSpecDataParam sInParam, Detect_and_Logger *pTmp) {
	if (sInParam.dTaskStartFreq < sInParam.dDataBeginFreq ||
		sInParam.dTaskStartFreq > sInParam.dDataBeginFreq + nIntLen*sInParam.dFreqReso ||
		sInParam.dTaskStartFreq > sInParam.dTaskEndFreq) {
		pTmp->loger_p->log_info("���õ���ʼƵ�ʺͽ���Ƶ�������ݲ�ƥ��");
		return 4;
	}

	float x = sInParam.dDataBeginFreq*
					sInParam.dFreqReso*
					sInParam.dTaskStartFreq*
					sInParam.dTaskEndFreq*
					sInParam.d3dBBw*
					sInParam.dCNThreshold*
					sInParam.dBwThreshold;

	if (x <= 0) {
		return 5;
	}

	if (sInParam.nMeanOrMax < 0 || sInParam.nMeanOrMax > 1) {
		return 5;
	}
		
	return 0;

}

void *CreateCCarrierDetectClass()
{
	//===========================================================================================
	std::map<std::string, std::string> mapConfigInfo;
	ConfigFileRead(mapConfigInfo);

	// ��־·����Ϊ��ʱ��ָ��λ�ã���ʹ��Ĭ��Ȩ��·��������ǰ·��/Logs/Log_yy-mm-dd_CarrierDetectDLL.txt"��
	std::string log_file_path = findValueFromMap(mapConfigInfo, "log_file_path");

	// ��־����  true: ������־�� false����������־
	bool create_log = false;
	std::string tmp_ = findValueFromMap(mapConfigInfo, "create_log");
	if (tmp_ == "true") create_log = true;

	// ģ��Ȩ��·����Ϊ��ʱ��ָ��λ�ã���ʹ��Ĭ��Ȩ��·��������ǰ·��/band_detect_torch.pt"��
	std::string model_path = findValueFromMap(mapConfigInfo, "model_path");

	//===========================================================================================
	//������־�ļ�
	if (log_file_path.empty()) {
		log_file_path = createDefaultLogFile();
	}

	//����Ȩ���ļ�, �����������
	if (model_path.empty()) {
		model_path = getDefaultModelPath();
	}

	Detect_and_Logger *ptr;
	try {
		ptr = new Detect_and_Logger(model_path, log_file_path, create_log);
	}
	catch (const std::bad_alloc ex)	{
		std::cerr << "=====�ڴ�������:" << ex.what() << std::endl;
		delete ptr;
	}

	return ptr;
}

void DeleteCCarrierDetectClass(void * pObj)
{
	delete pObj;
	//delete carrier_logger;
}


int CarrierDetectProInterface(void * pObj, char * pInData, int nInLen, InSpecDataParam sInParam, SP_Signal * sResult, int & nSigNum)
{
	Detect_and_Logger *pTmp = (Detect_and_Logger *)pObj;

	double right_freq_res = (sInParam.dTaskEndFreq - sInParam.dTaskStartFreq) / (nInLen / 2);

	pTmp->detect_p->set_data(pInData, sInParam.nMeanOrMax, nInLen);
	pTmp->detect_p->set_cnr_threshold(sInParam.dCNThreshold);
	pTmp->detect_p->set_least_band_width(sInParam.dBwThreshold, right_freq_res);
	std::vector<band_info> results = pTmp->detect_p->detect();

	nSigNum = results.size();
	memset(sResult, 0, nSigNum * sizeof(SP_Signal));

	SP_Signal tmp_sig;
	for (int i = 0; i < nSigNum; ++i) {
		tmp_sig.dCN = results[i].cnr;
		tmp_sig.dSignalLevel = results[i].amptitude;
		tmp_sig.dFreqBegin = results[i].x * right_freq_res + sInParam.dTaskStartFreq;
		tmp_sig.dFreqEnd = results[i].y * right_freq_res + sInParam.dTaskStartFreq;
		tmp_sig.dBW = tmp_sig.dFreqEnd - tmp_sig.dFreqBegin;
		tmp_sig.dFreqMid = tmp_sig.dFreqBegin + tmp_sig.dBW / 2;

		//sResult[i] = tmp_sig;
		memcpy((char *)sResult + i * sizeof(tmp_sig), &tmp_sig, sizeof(tmp_sig));
	}

	return 0;
}


//�������ܣ��ز���Ⲣ���ظö�Ƶ����Ч��ֹƵ��
//����ֵ:
//0������
//-6������ز������������ָ��ֵ
//-5�������������
//-4�����õ���ʼƵ�ʺͽ���Ƶ�������ݲ�ƥ��
//-3���ز���⺯������
//-2���ҵ������
//-1���ڴ����ʧ��	
int  CarrierDetectAndCheckValidFreqProInterface(void* pObj, char *pInData, int nInLen, InSpecDataParam sInParam, SP_Signal* sResult, int &nSigNum, double &dSpecValidEndFreq) 
{
	//return 0;  // �����ã�����
	Detect_and_Logger *pTmp = (Detect_and_Logger *)pObj;

	int inputArgsCheck = checkoutInputArgs(nInLen, sInParam, pTmp);
	if (inputArgsCheck) {
		nSigNum = 0;
		pTmp->loger_p->log_info("��������{}��4�����õ���ʼƵ�ʺͽ���Ƶ�������ݲ�ƥ�䣬 5�������������", inputArgsCheck);
		return inputArgsCheck;
	}
	char buf[1024];
	//info2log(log_file_name, "\n��ڲ�����\n");
	pTmp->loger_p->log_info("��ڲ�����");

	sprintf(buf, "�������ݳ��� = %d\n", nInLen);
	pTmp->loger_p->log_info(buf);
	pTmp->loger_p->log_info("�����������{}", nSigNum);

	sprintf(buf, "\n\t������ʼƵ�� =\t%2f\n\t�ֱ��� =\t%2f\n\t����ʼƵ�� =\t%2f\n\t�������Ƶ�� =\t%2f",
		sInParam.dDataBeginFreq,
		sInParam.dFreqReso,
		sInParam.dTaskStartFreq,
		sInParam.dTaskEndFreq);
	pTmp->loger_p->log_info(buf);

	sprintf(buf, "\n\t�źŴ������� =\t%2f\n\t��������� =\t%2f\n\t�������� =\t%2f\n\tƽ��ֵ���ֵѡ�� =\t%d\n",
		sInParam.d3dBBw,
		sInParam.dCNThreshold,
		sInParam.dBwThreshold,
		sInParam.nMeanOrMax);
	pTmp->loger_p->log_info(buf);


	double right_freq_res = sInParam.dFreqReso; // (sInParam.dTaskEndFreq - sInParam.dTaskStartFreq) / (nInLen / 2);

	pTmp->detect_p->set_data(pInData, sInParam.nMeanOrMax, nInLen);
	pTmp->detect_p->set_cnr_threshold(sInParam.dCNThreshold);
	pTmp->detect_p->set_least_band_width(sInParam.dBwThreshold, right_freq_res);
	std::vector<band_info> results = pTmp->detect_p->detect();

	int stop_point = nInLen / 2;  // ��ʼΪ�������ݳ���

	if (!results.empty()) {
		float left_min = 0.;
		float right_min = 0.;
		band_info last_band = results.back();

		pTmp->loger_p->log_debug("len(results) = {}", results.size());
//#ifdef _DEBUG
//		std::cout << "len(results) = " << results.size() << std::endl;
//#endif // DEBUG

		int last_band_width = last_band.y - last_band.x;
		pTmp->detect_p->calculate_min(last_band_width, left_min, right_min, last_band);


		//std::vector<int>::iterator begin, end;
		std::vector<float> data_v;
		if (left_min < right_min) {
//#ifdef _DEBUG
//			printf("left_min < right_min\n");
//			printf("last_band.x = %d\n", last_band.x);
//#endif // DEBUG
			pTmp->loger_p->log_debug("left_min < right_min ==>> last_band.x = {}", last_band.x);
			if (last_band.amptitude - right_min < sInParam.dCNThreshold - 1) {
				results.pop_back();  //ɾ�����һ���ز����

				int min_w = int(last_band_width * 0.1);
				data_v = std::vector<float>(pInData, pInData + nInLen);

				if (last_band.x - min_w < 0) {
					std::reverse(data_v.begin(), data_v.begin() + last_band.x + 1);
					stop_point = last_band.x - std::distance(data_v.begin(),
						std::min_element(data_v.begin(), data_v.begin() + last_band.x + 1));
				}
				else {
					std::vector<float> tmp_data_v = std::vector<float>(data_v.begin() + last_band.x - min_w,
						data_v.begin() + last_band.x + 1);
					std::reverse(tmp_data_v.begin(), tmp_data_v.end());
					stop_point = last_band.x - std::distance(tmp_data_v.begin(),
						std::min_element(tmp_data_v.begin(), tmp_data_v.end()));

					pTmp->loger_p->log_debug("min_w = {}\ttmp_stop_point = {}", min_w,
						std::distance(tmp_data_v.begin(), std::min_element(tmp_data_v.begin(), tmp_data_v.end())));
					pTmp->loger_p->log_debug("len(results) = {}", results.size());
//#ifdef _DEBUG
//					printf("min_w = %d\n tmp_stop_point = %d\n", min_w,
//						std::distance(tmp_data_v.begin(),
//							std::min_element(tmp_data_v.begin(), tmp_data_v.end())));
//					std::cout << "len(results) = " << results.size() << std::endl;
//#endif // DEBUG

				}
			}

			// ����ֹ�㲻�������ܳ�ʱ�����¼���
			dSpecValidEndFreq = sInParam.dTaskStartFreq + right_freq_res*stop_point;  // ��ֹƵ��  
		}
		else {  // ��ֹ���������ܳ�ʱ��ֱ�ӷ���������ֹƵ��
			dSpecValidEndFreq = sInParam.dTaskEndFreq;
		}

		pTmp->loger_p->log_debug("��ֹƵ�� = {}", stop_point);
//#ifdef _DEBUG
//		printf("��ֹƵ�㣺%d\n", stop_point);
//#endif // DEBUG

	}

	if (nSigNum <= results.size()) {
		pTmp->loger_p->log_info("����ز�����[{}]�������ָ��ֵ[{}]", results.size(), nSigNum);
		return 6;
	}

	nSigNum = results.size();
	memset(sResult, 0, nSigNum*sizeof(SP_Signal));

	sprintf(buf, "����ز����� = %d\n", nSigNum);
	pTmp->loger_p->log_info(buf);

	//sResult = (SP_Signal *)malloc(m_nSigNum * sizeof(SP_Signal));
	SP_Signal tmp_sig;
	for (int i = 0; i < nSigNum; ++i) {
		tmp_sig.dCN = results[i].cnr;
		tmp_sig.dSignalLevel = results[i].amptitude;
		tmp_sig.dFreqBegin = results[i].x * right_freq_res + sInParam.dTaskStartFreq;
		tmp_sig.dFreqEnd = results[i].y * right_freq_res + sInParam.dTaskStartFreq;
		tmp_sig.dBW = tmp_sig.dFreqEnd - tmp_sig.dFreqBegin;
		tmp_sig.dFreqMid = tmp_sig.dFreqBegin + tmp_sig.dBW / 2;

		//sResult[i] = tmp_sig;
		memcpy((char *)sResult + i*sizeof(tmp_sig), &tmp_sig, sizeof(tmp_sig));

		sprintf(buf, "\%3d:\t�����=%.3f dB\t��ƽ=%.3f dB\t��ʼƵ��=%.3f MHz\t����Ƶ��=%.3f MHz\t����=%.3f MHz\t����Ƶ��=%.3f MHz",
			i,
			tmp_sig.dCN,
			tmp_sig.dSignalLevel,
			tmp_sig.dFreqBegin,
			tmp_sig.dFreqEnd,
			tmp_sig.dBW,
			tmp_sig.dFreqMid);
		pTmp->loger_p->log_info(buf);
	}

	sprintf(buf, "��ֹƵ��=%3f MHz\n", dSpecValidEndFreq);
	pTmp->loger_p->log_info(buf);

	return 0;
}