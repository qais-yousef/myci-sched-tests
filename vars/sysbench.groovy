def call(iterations, numthreads, delay, csv) {
	sh """
		echo "events_per_second" > ${csv}

		for i in \$(seq ${iterations})
		do
			uclampset -M 0 sysbench --threads=${numthreads} --test=cpu run 2>/dev/null |
				grep "events per second" |
				awk -F : '{print \$2}' |
				xargs >> ${csv}

			sleep ${delay}
		done
	"""
}
