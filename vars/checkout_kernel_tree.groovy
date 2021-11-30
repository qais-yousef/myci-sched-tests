def call() {
	sh """
		if [ ! -d linux ]; then
			git clone https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git
		fi

		pushd linux
		git fetch
		popd
	"""
}
