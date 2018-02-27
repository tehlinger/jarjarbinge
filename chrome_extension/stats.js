var panel = null
var panel_never_loaded = true;
var last_res = null;

EXTENSION = "mdaahbifddgcfhaibfkfpeiombojjfhe"
CHECK_FREQUENCY = Math.floor((1000/24)*0.75)

//If t doesn't contain '@', it means that the
//'Stats for nerds' panel is not ready yet.
function res_is_loaded(t){
	return t.indexOf("@") != -1;
}

//Compare to dicts
function different_res(d1,d2){
	return JSON.stringify(d1) != JSON.stringify(d2);
}

//Sends the resolution to the extension background,
//the main part of the program
function send_res(r){
	chrome.runtime.sendMessage(EXTENSION,{'cmd': 'new_res','res':res_dic});
}

//Extract the interesting data out of the "Stats for nerds"
//HTML panel and puts it in a pretty dictionnary.
function resolution_data(res_text,panel_html){
		res_text = res_text.slice(res_text.indexOf("1"))
		res_values = res_text.replace(/\s+/g, '').split('/');
		codecs_text = panel_html.children[4].textContent;
		return {"optimal_res":res_values[1],
			"true_res":res_values[0],
			"codecs":codecs_text}
}

//Inspects the "Stats for nerds" panel HTML and returns
//null if it's not ready. Otherwise, returns a dictionnary
//with the intersting data.
function parse_panel(panel){
	panel_html = panel[0].childNodes[1];
	res_text = panel_html.children[2].textContent;
	if(res_is_loaded(res_text)){
		dic = resolution_data(res_text,panel_html)
		return dic;
	}
	else{
		return null;
	}
}

//Keeps trying to inspects the "Stats for nerds" panel
//when it's ready, sends the data
function keep_trying_to_get_panel(){
	d = document.getElementsByClassName('html5-video-info-panel');
	//Panel not ready
	if(d.length != 0){
	//Panel ready, but data maybe not loaded.
		res_dic = parse_panel(d)
		if (res_dic != null){
			if (panel_never_loaded ||
				different_res(last_res,res_dic)){
					panel_never_loaded = false;
					last_res = res_dic
					send_res(res_dic);
			}
			}
		}
		setTimeout(keep_trying_to_get_panel,CHECK_FREQUENCY);
	}

keep_trying_to_get_panel()
