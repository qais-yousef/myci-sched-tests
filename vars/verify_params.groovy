def call(extra_checks=false) {
	if (!env.ITERATIONS || !env.DELAY || extra_checks) {
		error('Some params are missing, refresh the page and try again')
	}

	switch (env.MYCI_NODE_TYPE) {
	case "android":
		if (!env.RUN_DEX2OAT) {
			error('Some params are missing, refresh and try again')
		}
		break
	case "linux":
		break
	default:
		break
	}
}
