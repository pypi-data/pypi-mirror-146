import json

class BaseData():
    def __init__(self, json_dict):
        self.json_dict = json_dict

    def to_json(self):
        # if it's not a dict, treat it as string. therefore it needs to load string as json.
        return_value = self.json_dict if type(self.json_dict) is dict else json.loads(self.json_dict) 
        return return_value

class Model(BaseData):
    '''
        - benchmark_list_uri: [string] GET request URI to get all model benchmarks of the model.
        - created: [string] date time string in UTC.
        - download_uri: [string] download URI from current gateway.
        - local_path: [string]
        - name: [string] model display name.
        - size: [integer] model file size in bytes.
        - start_benchmark_uri: [string] POST request URI to start the benchmark of the model.
        - type: [string] type of model. (ex: tflite, h5)
        - user_id: [string] unique user identifier who uploaded.
        - uuid: [string] unique model identifier.
        - available_nodes: list of nodes that can run benchmark of the model.
        - compiler_version: [string] compiler version used to compile the model.
        - parent_model_uuid: [string] if this model is converted model from a model, this property shows the uuid of original model.
        - has_file: [boolean] if it's true, model has file.
    '''
    def __init__(self, model_data):
        super().__init__(model_data)
        self.available_nodes = []
        self.benchmark_list_uri = model_data.get("benchmark_list_uri", None)
        self.created = model_data.get("created", None)
        self.download_uri = model_data.get("download_uri", None)
        # self.id = model_data["id"]
        self.local_path = model_data.get("local_path", None)
        self.name = model_data.get("name", None)
        self.size = model_data.get("size", None)
        self.start_benchmark_uri = model_data.get("start_benchmark_uri", None)
        self.type = model_data.get("type", None)
        self.user_id = model_data.get("user_id", None)
        self.parent_model_uuid = model_data.get("parent_model_uuid", None)
        self.has_file = model_data.get("has_file", None)
        self.uuid = model_data.get("uuid", None)
        if(model_data.get("available_nodes", None) is not None):
            for node_data in model_data["available_nodes"]:
                self.available_nodes.append(Node(node_data))


class Node(BaseData):
    '''
        - active: [boolean] if it’s true, node is active.
        - available_model_types: [string] comma separated types (ex: “tflite, h5”)
        - cpu_info: [string] cpu information
        - installed_software_versions: [string] installed software version information.
        - ipaddress: [string] node’s ipaddress which gateway can reach.
        - last_connected: [string]
        - machine: [string] node’s architecture type
        - memory_in_use: [string] memory in MB
        - name: [string] display name of the node
        - port: [string] node’s port which device fram node server is binding.
        - power_fan_mode: [string] fan mode support status.
        - processor: [string] node’s processor name (can be empty)
        - processor_speed: [string] processor’s speed in Hz. 
                (some node can report in different format. ex: 2.4GHz)
        - ram: [float] RAM in MB
        - system: [string] node’s system (ex: Linux, Darwin)
        - uuid : [string] unique node id
        - version: [string] node’s system version
    '''
    def __init__(self, node_data):
        super().__init__(node_data)
        self.active = node_data.get("active", None)
        self.available_model_types = node_data.get("available_model_types", None)
        self.cpu_info = node_data.get("cpu_info", None)
        self.ipaddress = node_data.get("ipaddress", None)
        self.installed_software_versions = node_data.get("installed_software_versions", None)
        self.last_connected = node_data.get("last_connected", None)
        self.machine = node_data.get("machine", None)
        self.memory_in_use = node_data.get("memory_in_use", None)
        self.name = node_data.get("name", None)
        self.port = node_data.get("port", None)
        self.power_fan_mode = node_data.get("power_fan_mode", None)
        self.processor = node_data.get("processor", None)
        self.processor_speed = node_data.get("processor_speed", None)
        self.ram = node_data.get("ram", None)
        self.system = node_data.get("system", None)
        self.uuid = node_data.get("uuid", None)
        self.version = node_data.get("version", None)

class Benchmark(BaseData):
    '''
        - callback_url: [max 512byte string] every time when there is task status update, 
                the gateway will send (POST) the benchmark json object to the given url.
        - cancelled_task_count: [int] count of tasks which are failed on a node.
        - compiling_task_count: [int] count of tasks which are compiling on a node.
        - created: [string] date time string in UTC.
        - downloading_task_count: [int] count of tasks which are downloading models on a node.
        - ended_task_count: [int] count of tasks which are finished without error on a node.
        - model_uuid: [string] model unique identifier
        - running_task_count: [int] count of tasks which are running on a node.
        - task_node_pairs: [Node, Task] array of Node Object and Task Object pairs
        - user_id: [string] user’s unique identifier who requested the benchmark
        - uuid: [string] benchmark unique identifier
        - waiting_task_count: [int] count of tasks which are in the queue on a node.
    '''
    def __init__(self, bench_data):
        super().__init__(bench_data)
        self.callback_url = bench_data.get("callback_url", None)
        self.cancelled_task_count = bench_data.get("cancelled_task_count", None)
        self.compiling_task_count = bench_data.get("compiling_task_count", None)
        self.created = bench_data.get("created", None)
        self.downloading_task_count = bench_data.get("downloading_task_count", None)
        self.ended_task_count = bench_data.get("ended_task_count", None)
        self.model_uuid = bench_data.get("model_uuid", None)
        self.running_task_count = bench_data.get("running_task_count", None)
        task_node_pairs_data = []
        if bench_data.get("task_node_pairs", None) is not None:
            for i in range(0, len(bench_data["task_node_pairs"])):
                task_node_pairs_data.append(Task_Node_Pair(bench_data["task_node_pairs"][i]))
        else:
            task_node_pairs_data = None
        self.task_node_pairs = task_node_pairs_data
        self.user_id = bench_data.get("user_id", None)
        self.uuid = bench_data.get("uuid", None)
        self.waiting_task_count = bench_data.get("waiting_task_count", None)

class Task(BaseData):
    '''
        - additional_options: [string(max 512 bytes)] additional option string for benchmark 
                (for ‘trt’ and ‘onnx-trt’ ex: –workspace=2048)
        - benchmark_uuid: [string] unique benchmark identifier
        - callback_url: [string]
        - compilation_ended: [string] date time string in UTC.
        - compilation_started: [string] date time string in UTC.
        - compiler_version: [string] compiler version used to compile the model.
        - convert_additional_options: [string] convert additional option string for conversion.
        - converted_model_uuid: [uuid] if this task converts the original model to a another type of model, 
                this property shows the uuid of converted model.
        - enable_op_profiling: [boolean] always true.
        - error: [string] if there is an error while benchmarking, this will show the reason.
        - inference_result: inference result json object.
        - max_secs: [integer] max benchmark running time in seconds.
        - model_download_ended: [string] date time string in UTC.
        - model_download_started: [string] date time string in UTC.
        - model_type: [string] model type (ex: tflite)
        - model_url: [string] model download url. (node can download from this url)
        - model_uuid: [string] unique model identifier.
        - node_uuid: [string] unique node identifier
        - num_runs: [integer] number of inference runs.
        - num_threads: [integer] number of threads benchmark tool can use.
        - power_consumption_measurement: [boolean] power_consumption_measurement is for measuring power consumption.
                Currently, this feature is supported only on the Jetson series of boards.
        - power_consumption_result: [string] result of power consumption
        - profile_result: array of profile result json objects.
        - result_power_string: [string] power consumption string that contains “gpu(avg)” and “ gpu(max)”, and “cpu(avg)” and “cpu(max)” in mA.
        - result_string: [string]
        - status: [string] task status (waiting, downloading, compiling, running, ended, cancelled). 
                cancelled means there is an error occurred.
        - task_created: [string] date time string in UTC.
        - task_ended: [string] date time string in UTC.
        - task_started: [string] date time string in UTC.
        - use_gpu: [boolean] use gpu for inference. if the node doesn’t support gpu, it will be ignored.
        - use_xnnpack: [boolean]
        - uuid: [string] unique task identifier.
    '''
    def __init__(self, task_data):
        super().__init__(task_data)
        self.additional_options = task_data.get("additional_options", None)
        self.benchmark_uuid = task_data.get("benchmark_uuid", None)
        self.callback_url = task_data.get("callback_url", None)
        self.compilation_ended = task_data.get("compilation_ended", None)
        self.compilation_started = task_data.get("compilation_started", None)
        self.compiler_version = task_data.get("compiler_version", None)
        self.convert_additional_options = task_data.get("convert_additional_options", None)
        self.converted_model_uuid = task_data.get("converted_model_uuid", None)
        self.enable_op_profiling = task_data.get("enable_op_profiling", None)
        self.error = task_data.get("error", None)
        self.inference_result = Inference_Result(task_data["inference_result"]) if task_data["inference_result"] is not None else None
        self.max_secs = task_data.get("max_secs", None)
        self.model_download_ended = task_data.get("model_download_ended", None)
        self.model_download_started = task_data.get("model_download_started", None)
        self.model_type = task_data.get("model_type", None)
        self.model_url = task_data.get("model_url", None)
        self.model_uuid = task_data.get("model_uuid", None)
        self.node_uuid = task_data.get("node_uuid", None)
        self.num_runs = task_data.get("num_runs", None)
        self.num_threads = task_data.get("num_threads", None)
        self.power_consumption_measurement = task_data.get("power_consumption_measurement", None)
        self.power_consumption_result = Power_Consumption(task_data.get("power_consumption_result")) if task_data.get("power_consumption_result", None) is not None else None
        profile_data = task_data.get("profile_result", None)
        profile_results = []
        if profile_data is not None:
            for i in range(0, len(profile_data)):
                profile_results.append(Profile_Result(profile_data[i]))
        else:
            profile_results = None
        self.profile_result = profile_results
        self.result_power_string = task_data.get("result_power_string", None)
        self.result_string = task_data.get("result_string", None)
        self.status = task_data.get("status", None)
        self.task_created = task_data.get("task_created", None)
        self.task_ended = task_data.get("task_ended", None)
        self.task_started = task_data.get("task_started", None)
        self.use_gpu = task_data.get("use_gpu", None)
        self.use_xnnpack = task_data.get("use_xnnpack", None)
        self.uuid = task_data.get("uuid", None)

class Profile_Result(BaseData):
    '''
        - title: [string] name of profile section.
        - keys: [array of string] keys for profile value objects.
        - values: [array of profile value objects] it has the values that match with ‘keys’.
    '''
    def __init__(self, profile_data):
        super().__init__(profile_data)
        self.keys = None
        self.title = None
        self.values = None
        if profile_data != None:
            self.keys = profile_data.get("keys", None)
            self.title = profile_data.get("title", None)
            vals = []
            [vals.append(Value(profile_data['values'][i])) for i in range(0, len(profile_data['values']))]
            self.values = vals

class Value(BaseData):
    def __init__(self, value_data):
        super().__init__(value_data)
        self.per = None
        self.avg_ms = None
        self.cdf = None
        self.first = None
        self.memkb = None
        self.name = None
        self.start = None
        self.times_called = None
        self.node_type = None
        if value_data != None:
            self.per = value_data.get(" %", None)
            self.avg_ms = value_data.get(" avg_ms", None)
            self.cdf = value_data.get(" cdf%", None)
            self.first = value_data.get(" first", None)
            self.memkb = value_data.get(" mbm KB", None)
            self.name = value_data.get(" name", None)
            self.start = value_data.get(" start", None)
            self.times_called = value_data.get(" times called", None)
            self.node_type = value_data.get("node type", None)

class Inference_Result(BaseData):
    '''
        - infernect_timings: [json object] inference timing dictionary that contains “init”, 
                “warmup (avg)”, “first inference” and “inference (avg)” times in microseconds.
        - memory_footprints: [json object] memory footprint dictionary that contains “init” and “overall”, or “cpu” and “gpu” in MB.
    '''
    def __init__(self, inf_data):
        super().__init__(inf_data)
        self.inference_timings = None
        self.memory_footprints = None
        if inf_data != None:
            self.inference_timings = Inference_Timing(inf_data.get("inference_timings", None))
            self.memory_footprints = Memory_Footprint(inf_data.get("memory_footprints", None))

class Inference_Timing(BaseData):
    def __init__(self, tim_data):
        super().__init__(tim_data)
        self.first = None
        self.inference_avg = None
        self.init = None
        self.max = None
        self.median = None
        self.min = None
        self.warmup = None
        if tim_data != None:
            self.first = tim_data.get("first", None)
            self.inference_avg = tim_data.get("inference (avg)", None)
            self.init = tim_data.get("init", None)
            self.max = tim_data.get("max", None)
            self.median = tim_data.get("median", None)
            self.min = tim_data.get("min", None)
            self.warmup = tim_data.get("warmup (avg)", None)

class Memory_Footprint(BaseData):
    def __init__(self, mem_data):
        super().__init__(mem_data)
        self.init = None
        self.overall = None
        self.gpu = None
        self.cpu = None
        if mem_data != None:
            self.init = mem_data.get("init", None)
            self.overall = mem_data.get("overall", None)
            self.gpu = mem_data.get("gpu", None)
            self.cpu = mem_data.get("cpu", None)

class Task_Node_Pair(BaseData):
    def __init__(self, tnp_data):
        super().__init__(tnp_data)
        self.node = None
        self.task = None
        if tnp_data != None:
            self.node = Node(tnp_data.get("node", None))
            self.task = Task(tnp_data.get("task", None))

class Power_Consumption(BaseData):
    def __init__(self, pwr_data):
        super().__init__(pwr_data)
        self.power_consumption = None
        if pwr_data != None:
            self.power_consumption = Power_consumption_child(pwr_data.get("power_consumption", None))

class Power_consumption_child(BaseData):
    def __init__(self, pwr_data):
        super().__init__(pwr_data)
        self.cpu_gpu_avg = pwr_data.get("cpu-gpu (avg)", None)
        self.cpu_gpu_max = pwr_data.get("cpu-gpu (max)", None)
        self.cpu_avg = pwr_data.get("cpu (avg)", None)
        self.cpu_max = pwr_data.get("cpu (max)", None)
        self.gpu_avg = pwr_data.get("gpu (avg)", None)
        self.gpu_max = pwr_data.get("gpu (max)", None)