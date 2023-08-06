# <img src="../../hydrogen_icon.jpeg" alt="HydroGEN Icon" style="height: 25px"> HydroGEN Common

The hydrogen_common PIP package provides services to simplify the code of various components used in the hydrogen application. The services support for configuring logging and use of the hydogen message bus.

These shared functions not only simplfy the code, but they enforce common conventions on where logs are stored and conventions on how components communicate using the message bus. These conventions simplify the code and improve maintainability.

* hydrogen\_setup\_logger()
* MessageBus
* send\_request\_message()
* send\_publish\_message()
* listen\_on\_message\_bus()
* run\_job\_using\_callback()
* execute\_with\_class\_and\_reply()
* execute\_with\_function\_and\_reply()
* set\_message\_bus\_class()
* job_main()
* get_data_directory()
* get_domain_directory()

### Install
This component can be installed for python using the command:

	pip install git+ssh://git@github.com/hydroframe-ml/hydrogen-service.git
	
## Classes and Functions

### HydroGEN Setup Logger
Call this method once in a process to configure the python logger.

	from hydrogen_common import hydrogen_setup_logger
	
	hydrogen_setup_logger()

### Message Bus
This class supports connecting to the message bus and using the message bus. This class is mostly used internally, but the following is an example of how to use it to send a synchronous message to the bus and get a reply.

	from hydrogen_common import MessageBus
	import asyncio
	
	async with MessageBus() as bus:
		message = {argument: "value"}
		subject = 'targetcomponentname'
		reply = await bus.request(subject, json.dumps(message))
		response = json.loads(reply)
				

### Send Request Message
Use the send\_request\_message() function instead of directly using the MessageBus class to send a synchrouous json message and get a reply.

This is an asynchonous function which is required because of the message bus so this function must be called using asyncio.run() to be used synchronously.

	import asyncio
	from hydrogen_common import send_request_message
	
	message = {argument: "value"}
	response = asyncio.run(send_request_message(message, 'message_subject'))
	
### Send Publish Message
Use the send\_publish\_message() function to publish an asychronous json message using the Message Bus. 

This is an asynchonous function which is required because of the message bus so this function must be called using asyncio.run() to be used synchronously.

	import asyncio
	from hydrogen_common import send_publish_message
	
	message = {argument: "value"}
	response = asyncio.run(send_publish_message(message, 'message_subject'))

If there was an error trying to publish the message the response will contain {"status": "fail", "message": "error message"}

### Listen On Message Bus
The listen\_on\_message\_bus() function is used internally by wait\_for\_event() to subscribe and listen on the message bus for events. When an event is sent this invokes an asynchonous callback function to handle the event. This method listens forever so many events can be handled.

	from hydrogen_common import listen_on_message_bus
	
	import asyncio
	listen_on_message_bus('subject-name', callback)

### Run Job Using Callback
The run\_job\_using\_callback() function is used internally by wait\_for\_event() for a process that expects to be called by an Argo workflow. The same callback used by listen\_on\_message\_bus() can be used to execute the job except this method returns after the callback is complete so the job can exit as required by Argo components.

	from hydrogen_common import run_job_using_callback
	
	run_job_using_callback('subject-name', callback, ['arg1'])

In the example above the function invokes the callback function with a json message containing {'subject': 'subject-name', 'arg1': 'value of arg1 environment variable'}

The convention is that Argo workflow pass arguments by environment variables. This method gets the value of the environment variables puts them into a json message to be used by the callback. This allows the same callback function to be used when listening to the message bus.

### JobMain
Use the job\_main_() function in the main function of a process that listens to
the event bus or waits to be called by an argo workflow. Specify the callback that
is used for either run\_job\_using\_callback() or listen\_on\_message\_bus().
Specify the subject that should trigger this event and a list of environment variables
containing arguments if this event is invoked from Argo.

It is important to use this method for components that are triggered by the message bus whether they are triggered from Argo or by directly listening to the event bus. This method handles both scenarios and even allows the code to work if the message bus is not NATS, but is something else.

	from hydrogen_common import job_main

	if __name__ == '__main__':
	    job_main('subject_name', subscribe_callback, ["domain_path"])

The above example receives events for the subject_name and accepts arguments using
the 'domain_path' environment variable.


### Execute With Class And Reply
Use the execute\_with\_class\_and\_reply() method within the callback function passed to run\_job\_using\_callback() or listen\_on\_message_bus(). This supports a convention of implemeting a callback as a class with methods for various different message received by the subject. For example:

	import asyncio
	from hydrogen_common import execute_with_class_and_reply
	
	class MyClass:
		def get(self):
			return {'hello': 'world'}
			
	async def callback(message):
		json_message = json.loads(message.data)
		await execute_with_class_and_reply(MyClass(), message.subject, message.reply, json_message)
		
	if __name__ == '__main__':
		job_main('mysubject', callback) 
		
The value returned by the get() method is published back to the reply subject passed in the call. The execute\_with_class\_and\_reply() method can also be used for Argo asynchonous components to send a reply to any subject specified in the argument.  If the method raises an exception a reply is sent with a json message with the value {"status": "fail", "message": "error message"}.

The convention is that if the message contains the attribute 'op' with the value of a method name in the class then that method name will be invoked with the json message. So the above example assumes the message sent to the NATS message bus contained {"op": "get"} and any other arguments required by the get() method.

The class may also implement the method handle\_event(self, message) to handle message that do not contin an 'op' attribute or if there is no method in the class for the value of the 'op' attribute.

### Execute With Function And Reply

Use the execute\_with\_function\_and\_reply() method within the callback function passed to run\_job\_using\_callback() or listen\_on\_message_bus(). This is used when the implementation of the job is a single function and there is only one function for the subject of the event.

	import asyncio
	from hydrogen_common import execute_with_function_and_reply
			
	def do_work():
		return {"hello": "world"}
		
	async def callback(message):
		json_message = json.loads(message.data)
		await execute_with_function_and_reply(do_work, message.subject, 'reply_subject', json_message)
		
	if __name__ == '__main__':
		job_main('mysubject', callback) 

### Get Shared Directory
Use this to get the full path name to the shared directory in the environment in which
you are running using the configured environment variables.

### Get domain directory
Use this to get the full path name to the hydrogen domain directory for the specified user_id and domain_directory name that identifies a domain. This returns the path name
using the conventions of the current impementation.

    from hydrogen_common import get_domain_directory
	dir = get_domain_directory('myuser', 'domaindir1')
	
### Set Message Bus Class
Use the set\_message\_bus\_class() method within a unit test to set a mock implementation of the MessageBus class to be used by the other functions in hydrogen_common.

See unit tests for example of how this is used.

# Environment Variables
There are several environment variables that are assumed to be set by the functions in the hydrogen_common package. These variables are set by the Kubernetes and Docker Compose environments that run code. If you execute code in a local development environment you must set these enviroment variables yourself. These variables are set in the scripts in the ~/.hydrogen folder by the install scripts.

|Environment Variable|Purpose|
|------|-------|
|CONTAINER\_HYDRO\_DATA\_PATH|Path name of a directory where files are stored when the code is run within a docker container. The setup logger will create a logs subdirectory here if this directory exists.|
|HOST\_HYDRO\_DATA\_PATH|Path name of a directory where files are stored when the code is run within a kubernetes virtual machine. This is used for logs if the directory specified by CONTAINER\_HYDRO\_DATA\_PATH does not exist.|
|CLIENT\_HYDRO\_DATA\_PATH|Path name of a directory where files are stored when the code is run within the client machine outside of the virtual machine. This is used for logs if neither directory above eixsts.|





