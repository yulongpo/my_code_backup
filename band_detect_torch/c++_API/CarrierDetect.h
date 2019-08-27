/**************************************************************************
 * �汾: V1.0 ���Ƶ�׼�����ز���� 2017-02
 *     : V1.1 ���Ӽ������ڴ��������,����λ��ΪMHz 2017-03-23
 *     : V1.2 �����˲�ѡ����� 2017-04-19

/**************************************************************************/


#ifdef DLL_API
#else
#define DLL_API _declspec(dllimport)
#endif

#pragma once

#include "stdio.h"
#include <math.h>



struct SP_Signal
{
	double dFreqBegin;        //�ز���ʼƵ��,��λMHz
	double dFreqEnd;          //�ز�����Ƶ��,��λMHz
	double dFreqMid;          //�ز�����Ƶ��,��λMHz
	double dBW;               //�ز�����,��λMHz
	double dSignalLevel;      //�źŵ�ƽ,��λdBm
	double dCN;               //�����,��λdB

};


struct InSpecDataParam
{
	double dDataBeginFreq;	    //Ƶ�����ݵ���ʼƵ��,��λMHz
	double dFreqReso;            //Ƶ�����ݵķֱ���,��λMHz
	double dTaskStartFreq;       //����ʼƵ��,��λMHz
	double dTaskEndFreq;         //�������Ƶ��,��λMHz
	double d3dBBw;               //����źŴ�������,��λdB
	double dCNThreshold;         //������������,��λdB
	double dBwThreshold;         //����������,��λMHz
	char  nMeanOrMax;           //ƽ��ֵ���ֵѡ��  0��ʾƽ��ֵ 1��ʾ���ֵ����
	char  nFilterFlag;          //�Ƿ��˲�ѡ�� 0��ʾ���˲� 1��ʾ��Ҫ�˲�
	char  nInvertFlag;          //Ƶ���Ƿ�ȡ����־ 0��ʾ��ȡ�� 1��ʾȡ��

	double dFs;                  //������,��λMHz
	int   nFFTorder;            //FFT����
	int   nSmoothTimes;         //Ƶ��ƽ������
 };


//�������ܣ��ڶ�̬���д����ز�������ʵ��
extern "C"  _declspec(dllexport) void* CreateCCarrierDetectClass();

//�������ܣ��ڶ�̬����ɾ���ز���������ʵ��
extern "C"  _declspec(dllexport) void DeleteCCarrierDetectClass(void* pObj );

//�������ܣ��ز����
//����ֵ:
//0������
//-6������ز������������ָ��ֵ
//-5�������������
//-4�����õ���ʼƵ�ʺͽ���Ƶ�������ݲ�ƥ��
//-3���ز���⺯������
//-2���ҵ������
//-1���ڴ����ʧ��		
extern "C"  _declspec(dllexport) int  CarrierDetectProInterface(void* pObj,char *pInData,int nInLen,InSpecDataParam sInParam,SP_Signal* sResult,int &m_nSigNum);

//�������ܣ�Ƶ�׼���
//����ֵ:
//0������
//1��������������ƽ��������Ӧ����
//-2���ڴ����ʧ��
//-1�������������
extern "C" __declspec(dllexport)  int  SpecComputProInterface(void *pObj,char *pInData,int nInLen,InSpecDataParam sInParam,int &nSpecLen);

//�������ܣ�Ƶ���˲�
//����ֵ:
//0������
//1��������������ƽ��������Ӧ����
//-2���ڴ����ʧ��
//-1�������������
extern "C" __declspec(dllexport)  int  SpecAfterFilterInterface(void *pObj,char *pInData,int nInLen,InSpecDataParam sInParam,int &nSpecLen);
//�������ܣ��ز���Ⲣ���ظö�Ƶ����Ч��ֹƵ��
//����ֵ:
//0������
//-6������ز������������ָ��ֵ
//-5�������������
//-4�����õ���ʼƵ�ʺͽ���Ƶ�������ݲ�ƥ��
//-3���ز���⺯������
//-2���ҵ������
//-1���ڴ����ʧ��		
extern "C"  _declspec(dllexport) int  CarrierDetectAndCheckValidFreqProInterface(void* pObj,char *pInData,int nInLen,InSpecDataParam sInParam,SP_Signal* sResult,int &nSigNum,double &dSpecValidEndFreq);


