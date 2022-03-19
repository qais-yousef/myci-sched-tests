def call(extra_checks=false) {
	if (!env.NODE || extra_checks) {
		error('Parameters has changed, please refresh the page and try again')
	}

	switch (env.MYCI_NODE_TYPE) {
	case "android":
		if (!env.ITERATIONS || !env.DELAY || !env.RUN_DEX2OAT) {
			error('Parameters has changed, please refresh the page and try again')
		}
		break
	case "linux":
		break
	default:
		break
	}
}
