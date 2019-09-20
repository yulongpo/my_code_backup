#pragma once

#include <iostream>
#include "spdlog/spdlog.h"
#include "spdlog/sinks/basic_file_sink.h" // support for basic file logging
#include "spdlog/sinks/stdout_color_sinks.h"

using namespace spdlog;

class MyLogging {
public:
	//myLogging() {}
	MyLogging(std::string log_file_name = "CarrierDetectDLLLog.txt", 
		bool flg = true, bool truncate = false) 
		: log_file_name(log_file_name), 
		  logging_flg(flg){

		try
		{
			console_sink = std::make_shared<spdlog::sinks::stdout_color_sink_mt>();
			console_sink->set_level(spdlog::level::warn);
			console_sink->set_pattern("[%H:%M:%S] [%^DEBUG%$] %v");

			file_sink = std::make_shared<spdlog::sinks::basic_file_sink_mt>(log_file_name, truncate);
			file_sink->set_level(spdlog::level::trace);
			file_sink->set_pattern("[%H:%M:%S]  %v");

			info_logger = new logger("detect_logger", { file_sink });
			debug_logger = new logger("detect_logger", { console_sink, file_sink });

			//info_logger = basic_logger_mt("detect_logger", log_file_name, truncate);
			//set_default_logger(my_logger);
		}
		catch (const spdlog::spdlog_ex& ex)
		{
			std::cout << "Log initialization failed: " << ex.what() << std::endl;
		}
		//info_logger->set_pattern("[%H:%M:%S]  %v");
		//debug_logger->set_pattern("[%H:%M:%S] [%^%l%$] %v");
		set_log_level();
		debug_logger->set_level(spdlog::level::debug);
	}

	~MyLogging() {
		delete info_logger;
		delete debug_logger;
	}

	void set_log_level() {
		if (logging_flg) {
			info_logger->set_level(level::info);
		}
		else {
			info_logger->set_level(level::off);
		}
	}

	void set_enable(bool flg) {
		if (flg == logging_flg) {
			return;
		}
		info_logger->set_level(level::warn);
		info_logger->warn("******* SET LOGGING ENABLE FROM {} to {} *******", logging_flg, flg);
		logging_flg = flg;
		set_log_level();
	}

	void log_info(std::string info_msg) {
		if (logging_flg) {
			info_logger->info(info_msg);
		}
	}

	template<typename... Args>
	void log_info(string_view_t fmt, const Args &... args)
	{
		if (logging_flg) {
			info_logger->info(fmt, args...);
		}
	}

	void log_debug(std::string debug_msg) {
#ifdef _DEBUG
		debug_logger->warn(debug_msg);
#endif //_DEBUG
	}

	template<typename... Args>
	void log_debug(string_view_t fmt, const Args &... args)
	{
#ifdef _DEBUG
		debug_logger->warn(fmt, args...);
#endif //_DEBUG
	}


private:
	logger *info_logger;
	logger * debug_logger;

	std::string log_file_name;
	bool logging_flg = true;

	std::shared_ptr<spdlog::sinks::stdout_color_sink_mt> console_sink;
	std::shared_ptr<spdlog::sinks::basic_file_sink_mt> file_sink;
	//spdlog::logger logger("multi_sink", { console_sink, file_sink });
	//logger info_logger("logger", { file_sink });
	//logger debug_logger;


};