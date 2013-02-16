#include <stdio.h>

#include <string>

#include <Python.h>

#include <windows.h>

std::string getScriptPath() {
	std::string fileName;
	fileName.resize(MAX_PATH);
	DWORD size = GetModuleFileNameA(NULL, &fileName[0], fileName.size());
	fileName.resize(size);
	printf("%-10s: %s\n", "executable", fileName.c_str());
	std::string prefix = "\\\\?\\";
	if (fileName.size() > prefix.size() && fileName.substr(0, prefix.size()) == prefix) {
		fileName = fileName.substr(prefix.size(), fileName.size() - prefix.size());
	}
	fileName += ".py";
	printf("%-10s: %s\n", "script", fileName.c_str());
	return fileName;
}

void execfile(std::string scriptPath) {
	FILE* fp = fopen(scriptPath.c_str(), "rb");
	if (fp == NULL) {
		fprintf(stderr, "open script file failed. file: %s\n", scriptPath.c_str());
		return;
	}
	std::string s;
	int c;
	while((c = fgetc(fp)) != EOF) {
		s += (char)c;
	}
	fclose(fp);

	PyRun_SimpleString(s.c_str());
}

int main(int argc, char* argv[]) {
	//Py_SetProgramName("winrun-server");
	std::string scriptPath = getScriptPath();
	Py_Initialize();
	PySys_SetArgvEx(argc, argv, 0);
	execfile(scriptPath);
	Py_Finalize();
	return 0;
}
