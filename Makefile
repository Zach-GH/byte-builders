curr_dir= ../..
tc_dir= game/trivial_compute
icon= assets/sprites/icons/icon.ico

# auto-install the necessary packages
setup_tc: ${tc_dir}/requirements.txt
	pip install -r ${tc_dir}/requirements.txt

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

# package all directory files for release
release_tc: clean_tc
	@cd ${tc_dir}; \
	pyinstaller main.py --onefile --name ByteBuddies --noconsole -i ${icon}; \
	mkdir -p ${curr_dir}/release; \
	cp -rf assets ${curr_dir}/release/; \
	mv dist/ByteBuddies.app ${curr_dir}/release/; \
	cd ${curr_dir}; zip -r tc.zip release/*; \
	mv tc.zip release

# trivial compute run options
run_tc: main
run_win_tc: main_w
run_tc_1440: main_1440
run_tc_1080: main_1080

main:
	@make main -C game/trivial_compute

# windows option
main_w:
	@make main_w -C game\trivial_compute

main_1440:
	@make main_1440 -C game/trivial_compute

main_1080:
	@make main_1080 -C game/trivial_compute
