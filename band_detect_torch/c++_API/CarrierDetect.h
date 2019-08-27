/**************************************************************************
 * 版本: V1.0 完成频谱计算和载波检测 2017-02
 *     : V1.1 增加检测输出内存溢出保护,带宽单位改为MHz 2017-03-23
 *     : V1.2 增加滤波选择控制 2017-04-19

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
	double dFreqBegin;        //载波开始频点,单位MHz
	double dFreqEnd;          //载波结束频点,单位MHz
	double dFreqMid;          //载波中心频点,单位MHz
	double dBW;               //载波带宽,单位MHz
	double dSignalLevel;      //信号电平,单位dBm
	double dCN;               //载噪比,单位dB

};


struct InSpecDataParam
{
	double dDataBeginFreq;	    //频谱数据的起始频率,单位MHz
	double dFreqReso;            //频谱数据的分辨率,单位MHz
	double dTaskStartFreq;       //任务开始频率,单位MHz
	double dTaskEndFreq;         //任务结束频率,单位MHz
	double d3dBBw;               //检测信号带宽设置,单位dB
	double dCNThreshold;         //检测载噪比门限,单位dB
	double dBwThreshold;         //检测带宽门限,单位MHz
	char  nMeanOrMax;           //平均值最大值选择  0表示平均值 1表示最大值保持
	char  nFilterFlag;          //是否滤波选择 0表示不滤波 1表示需要滤波
	char  nInvertFlag;          //频谱是否取反标志 0表示不取反 1表示取反

	double dFs;                  //采样率,单位MHz
	int   nFFTorder;            //FFT阶数
	int   nSmoothTimes;         //频谱平滑次数
 };


//函数功能：在动态库中创建载波检测类的实例
extern "C"  _declspec(dllexport) void* CreateCCarrierDetectClass();

//函数功能：在动态库中删除载波检测类类的实例
extern "C"  _declspec(dllexport) void DeleteCCarrierDetectClass(void* pObj );

//函数功能：载波检测
//返回值:
//0－正常
//-6－输出载波个数大于最大指定值
//-5－输入参数错误
//-4－设置的起始频率和结束频率与数据不匹配
//-3－载波检测函数出错
//-2－找底噪出错
//-1－内存分配失败		
extern "C"  _declspec(dllexport) int  CarrierDetectProInterface(void* pObj,char *pInData,int nInLen,InSpecDataParam sInParam,SP_Signal* sResult,int &m_nSigNum);

//函数功能：频谱计算
//返回值:
//0－正常
//1－数据量不够，平滑次数相应减少
//-2－内存分配失败
//-1－输入参数错误
extern "C" __declspec(dllexport)  int  SpecComputProInterface(void *pObj,char *pInData,int nInLen,InSpecDataParam sInParam,int &nSpecLen);

//函数功能：频谱滤波
//返回值:
//0－正常
//1－数据量不够，平滑次数相应减少
//-2－内存分配失败
//-1－输入参数错误
extern "C" __declspec(dllexport)  int  SpecAfterFilterInterface(void *pObj,char *pInData,int nInLen,InSpecDataParam sInParam,int &nSpecLen);
//函数功能：载波检测并返回该段频谱有效截止频率
//返回值:
//0－正常
//-6－输出载波个数大于最大指定值
//-5－输入参数错误
//-4－设置的起始频率和结束频率与数据不匹配
//-3－载波检测函数出错
//-2－找底噪出错
//-1－内存分配失败		
extern "C"  _declspec(dllexport) int  CarrierDetectAndCheckValidFreqProInterface(void* pObj,char *pInData,int nInLen,InSpecDataParam sInParam,SP_Signal* sResult,int &nSigNum,double &dSpecValidEndFreq);


