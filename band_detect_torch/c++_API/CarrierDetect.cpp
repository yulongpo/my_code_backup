#include "CarrierDetect.h"
#include "WaveBandDetect.h"
#include <direct.h>

#include <algorithm>
#include <iterator>


void *CreateCCarrierDetectClass()
{
	char *buffer;
	std::string model_path;
	//也可以将buffer作为输出参数
	if ((buffer = _getcwd(NULL, 0)) == NULL)
	{
		perror("无法加载模型：获取当前地址错误！");
	}
	else
	{
		model_path = std::string(buffer);
		delete buffer;
	}

	model_path += "\\band_detect_torch.pt";
	return new WaveBandDetct(model_path);
}

void DeleteCCarrierDetectClass(void * pObj)
{
	delete pObj;
}

//int _CarrierDetectProInterface(WaveBandDetct *pObj, char *pInData, int nInLen, InSpecDataParam sInParam, SP_Signal *sResult, int & m_nSigNum) {
//	
//}

int CarrierDetectProInterface(void * pObj, char * pInData, int nInLen, InSpecDataParam sInParam, SP_Signal * sResult, int & m_nSigNum)
{
	WaveBandDetct *pTmp = (WaveBandDetct *)pObj;
	pTmp->set_data(pInData, nInLen);
	pTmp->set_cnr_threshold(sInParam.dCNThreshold);
	pTmp->set_least_band_width(sInParam.dBwThreshold, sInParam.dFreqReso);
	std::vector<band_info> results = pTmp->detect();

	m_nSigNum = results.size();

	//sResult = (SP_Signal *)malloc(m_nSigNum * sizeof(SP_Signal));
	SP_Signal tmp_sig;
	for (int i = 0; i < m_nSigNum; ++i) {
		tmp_sig.dCN = results[i].cnr;
		tmp_sig.dSignalLevel = results[i].amptitude;
		tmp_sig.dFreqBegin = results[i].x * sInParam.dFreqReso + sInParam.dTaskStartFreq;
		tmp_sig.dFreqEnd = results[i].y * sInParam.dFreqReso + sInParam.dTaskStartFreq;
		tmp_sig.dBW = tmp_sig.dFreqEnd - tmp_sig.dFreqBegin;
		tmp_sig.dFreqMid = tmp_sig.dFreqBegin + tmp_sig.dBW / 2;

		sResult[i] = tmp_sig;
	}

	return 0;
}


int  CarrierDetectAndCheckValidFreqProInterface(void* pObj, char *pInData, int nInLen, InSpecDataParam sInParam, SP_Signal* sResult, int &nSigNum, double &dSpecValidEndFreq) 
{
	WaveBandDetct *pTmp = (WaveBandDetct *)pObj;
	pTmp->set_data(pInData, nInLen);
	pTmp->set_cnr_threshold(sInParam.dCNThreshold);
	pTmp->set_least_band_width(sInParam.dBwThreshold, sInParam.dFreqReso);
	std::vector<band_info> results = pTmp->detect();

	int stop_point = nInLen;

	if (!results.empty()) {
		float left_min = 0.;
		float right_min = 0.;
		band_info last_band = results.back();
#ifdef DEBUG
		std::cout << "len(results) = " << results.size() << std::endl;
#endif // DEBUG

		int last_band_width = last_band.y - last_band.x;
		pTmp->calculate_min(last_band_width, left_min, right_min, last_band);


		//std::vector<int>::iterator begin, end;
		std::vector<float> data_v;
		if (left_min < right_min) {
#ifdef DEBUG
			printf("left_min < right_min\n");
			printf("last_band.x = %d\n", last_band.x);
#endif // DEBUG

			if (last_band.amptitude - right_min < sInParam.dCNThreshold - 1) {
				results.pop_back();  //删掉最后一个载波结果

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

					//std::reverse(data_v.begin() + last_band.x - min_w, data_v.begin() + last_band.x + 1);
					//stop_point = 2*last_band.x - min_w - std::distance(data_v.begin(),
					//	std::min_element(data_v.begin() + last_band.x - min_w, data_v.begin() + last_band.x + 1));
#ifdef DEBUG
					printf("min_w = %d\n tmp_stop_point = %d\n", min_w,
						std::distance(tmp_data_v.begin(),
							std::min_element(tmp_data_v.begin(), tmp_data_v.end())));
					std::cout << "len(results) = " << results.size() << std::endl;
#endif // DEBUG

				}
			}
		}
#ifdef DEBUG
		printf("截止频点：%d\n", stop_point);
#endif // DEBUG

	}

	dSpecValidEndFreq = sInParam.dTaskStartFreq + sInParam.dFreqReso*stop_point;  // 截止频率

	nSigNum = results.size();
	//sResult = (SP_Signal *)malloc(m_nSigNum * sizeof(SP_Signal));
	SP_Signal tmp_sig;
	for (int i = 0; i < nSigNum; ++i) {
		tmp_sig.dCN = results[i].cnr;
		tmp_sig.dSignalLevel = results[i].amptitude;
		tmp_sig.dFreqBegin = results[i].x * sInParam.dFreqReso + sInParam.dTaskStartFreq;
		tmp_sig.dFreqEnd = results[i].y * sInParam.dFreqReso + sInParam.dTaskStartFreq;
		tmp_sig.dBW = tmp_sig.dFreqEnd - tmp_sig.dFreqBegin;
		tmp_sig.dFreqMid = tmp_sig.dFreqBegin + tmp_sig.dBW / 2;

		sResult[i] = tmp_sig;
	}


	return 0;
}