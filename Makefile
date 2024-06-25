curr_dir= ../..
tc_dir= game/trivial_compute

# auto-install the necessary packages
setup_tc: ${tc_dir}/requirements.txt
	pip install -r ${tc_dir}/requirements.txt

# package all directory files for release
release_tc:
	@cd ${tc_dir}; \
	pyinstaller -F --noconsole --windowed \
	main.py; \
	mkdir -p ${curr_dir}/release; \
	cp -rf assets ${curr_dir}/release/; \
	mv dist/main ${curr_dir}/release/; \
	cd ${curr_dir}; zip -r tc.zip release/*; \
	mv tc.zip release

# run your release
test_release_tc:
	@cd release; ./main

# run linter
lint_tc:
	@pylint --rcfile=.pylintrc ./game/trivial_compute/*.py

# clean all un-needed files from your repository
clean_tc:
	rm -rf ${tc_dir}/__pycache__ \
	${tc_dir}/build ${tc_dir}/dist \
	${tc_dir}/*.spec \
	release

# trivial compute run options
run_tc: main
run_tc_1440: main_1440
run_tc_1080: main_1080

main: ${tc_dir}/main.py
	@cd ${tc_dir}; \
	./$@.py -r max -m full;

main_1440: ${tc_dir}/main.py
	@cd ${tc_dir}; \
	./main.py -r med -m sized;

main_1080: ${tc_dir}/main.py
	@cd ${tc_dir}; \
	./main.py -r min -m windowed;
