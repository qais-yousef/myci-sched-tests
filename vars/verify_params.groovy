def call(extra_checks=false) {
	if (!env.NODE || extra_checks) {
		script {
			currentBuild.description = "${NODE}: Parameters has changed, please refresh the page and try again"
			currentBuild.result = 'ABORTED'
			error('Aborting the build, params has changed. Please refresh the page and try again.')
		}
	}

	switch (env.MYCI_NODE_TYPE) {
	case "android":
		break
	case "linux":
		break
	default:
		break
	}
}
