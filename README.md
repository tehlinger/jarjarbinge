# jarjarbinge
Jar jar binge : a tool for measuring quality of experience of services while
modifying network characteristics.

Jarjarbinge has three parts, which will run 3 different HTTP servers :
* `master` is the main server that chooses QoE/QoS conditions and coordinates the experiment
* `qoe_measurer` contains the different QoE mesurer servers code. Each server measures one kind of application.
* `traffic_measurer` contains the code for the server that sets the QoS for each experiment with `traffic control`
