def call(wload, csv) {
	sh """
		uclampset -M 0 taskset 0x1 sysbench --threads=1 --test=cpu --time=60 run &>/dev/null &

		sleep 5

		rm -f *-0.log

		rt-app ./rt-app/${wload}

		cat *-0.log | sed -r 's/\\s+/,/g' | sed 's/^,//' > ${csv}

		rm -f *-0.log

		wait
	"""
}
