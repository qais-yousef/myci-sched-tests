def call(uclamp_min, uclamp_max, csv) {
	sh """
		rm -f *-0.log

		uclampset -m ${uclamp_min} -M ${uclamp_max} rt-app ./rt-app/rampup-task.json

		cat *-0.log | sed '0,/^# Policy/d' | sed -r 's/\\s+/,/g' | sed 's/^,//' > ${csv}

		rm -f *-0.log
	"""
}
