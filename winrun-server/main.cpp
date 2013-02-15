#include <stdio.h>

#include <string>

#include <Python.h>

int main(int argc, char* argv[]) {
	//Py_SetProgramName("winrun-server");
	Py_Initialize();
	PySys_SetArgvEx(argc, argv, 0);
	FILE* fp = fopen("winrun-server.py", "rb");
	if (fp != NULL) {
		std::string s;
		int c;
		while((c = fgetc(fp)) != EOF) {
			s += (char)c;
		}
		fclose(fp);

		PyRun_SimpleString(s.c_str());
	}
	Py_Finalize();

	return 0;
}
