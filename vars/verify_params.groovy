def call(extra_checks=false) {
	if (!env.NODE || !env.DESCRIPTION || extra_checks) {
		script {
			currentBuild.description = "${NODE}: Parameters has changed, please refresh the page and try again"
			currentBuild.result = 'ABORTED'
			error('Aborting the build, params has changed. Please refresh the page and try again.')
		}
	}

	switch (env.MYCI_NODE_TYPE) {
	case "android":
		if (!env.ITERATIONS || !env.DELAY || !env.RUN_DEX2OAT) {
			script {
				currentBuild.description = "${NODE}: Parameters has changed, please refresh the page and try again"
				currentBuild.result = 'ABORTED'
				error('Aborting the build, params has changed. Please refresh the page and try again.')
			}
		}
		break
	case "linux":
		break
	default:
		break
	}
}
