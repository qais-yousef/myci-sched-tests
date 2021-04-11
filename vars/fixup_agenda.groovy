def call(agenda, str, value) {
	sh """
		sed -i 's/${str}/${value}/' ${agenda}
		cat ${agenda}
	"""
}
