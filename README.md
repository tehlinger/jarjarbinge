# jarjarbinge
Jar jar binge : a tool for measuring quality of experience of services while
modifying network characteristics.

Jarjarbinge has three parts, which will run 3 different HTTP servers :
	- a master, that chooses the QoS and the QoE to set up for a given
	  measure
	- a QoE measurer, that will run the application to measure and send the
	  results
	- a traffic controller, in charge of setting specific QoS features
	  using tc, netem and tbf
