def call() {
	sh """
		flock /tmp/perfetto.lock plotting/plot_kernel_compile_test.py
	"""
}
