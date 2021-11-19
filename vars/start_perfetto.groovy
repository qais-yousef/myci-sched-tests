def call(name) {
	sh """
		touch ${name}.perfetto-trace
		tracebox -o ${name}.perfetto-trace --txt -d -c ./tools/config.pbtx &> perfetto.pid
	"""
}
