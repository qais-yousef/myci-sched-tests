def call(test_name, quiet_period, run_dex2oat) {
	test =	build quietPeriod: quiet_period, job: test_name, \
		parameters: [string(name: 'NODE', value: params.NODE), \
			     string(name: 'DESCRIPTION', value: params.DESCRIPTION), \
			     booleanParam(name: 'COLLECT_PELT', value: params.COLLECT_PELT), \
			     booleanParam(name: 'COLLECT_UCLAMP', value: params.COLLECT_UCLAMP), \
			     string(name: 'BRANCH', value: params.BRANCH), \
			     booleanParam(name: 'RUN_DEX2OAT', value: run_dex2oat), \
			     string(name: 'ITERATIONS', value: params.ITERATIONS), \
			     string(name: 'DELAY', value: params.DELAY)]

	if (test.result == "SUCCESS") {
		dir = test_name
		if (run_dex2oat)
			dir += '-dex2oat'
		copyArtifacts filter: '*.png', fingerprintArtifacts: true, projectName: test_name, selector: specific(test.getNumber().toString()), target: dir
	}
}
