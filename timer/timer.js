

class Timer {
    constructor(callback_start, callback_stop, interval) {
        this.interval = interval;
        this.start_time = 0;       
        this.repeat = null; 
        this.counter = 0;  
        this.stop_time = 0; 
        this.callback_upon_start = callback_start; 
        this.callback_upon_stop = callback_stop;
        this.time_elapsed = 0; 
        this.run = null;  
    }

    start() {       
        this.start_time = Date.now();
        this.repeat = setInterval(this.callback_upon_start, this.interval, this);
    }

    stop() {
        this.stop_time = Date.now() - this.start_time;
        this.callback_upon_stop.call(this, this);
        clearTimeout(this.repeat);
    }

    reset(){
        this.start_time = Date.now();
        this.callback_upon_start.call(this, this);
        
    }

}

// parameter t is an instance of Timer 
function setText(timer_object){
    ms_elapsed = Date.now() - timer_object.start_time;
    
    const min_factor = 60*1000;
       
    let min = Math.floor(ms_elapsed / min_factor);
    let ms_left = ms_elapsed - (min * min_factor)   
    let sec = Math.floor(ms_left / 1000);
    let ms = ms_left - (sec*1000);
    ms = Math.floor(ms / 100);
    document.getElementById("timer-text").value = format_timer_text(min,sec,ms);
}

function display_results(timer_object){
    ms_elapsed = timer_object.stop_time;
    
    const min_factor = 60*1000;
       
    let min = Math.floor(ms_elapsed / min_factor);
    let ms_left = ms_elapsed - (min * min_factor)   
    let sec = Math.floor(ms_left / 1000);
    let ms = ms_left - (sec*1000);
    ms = Math.floor(ms / 100);
    document.getElementById(results_id).value = format_timer_text(min,sec,ms);
}

function format_timer_text(min, sec, ms){
    let = minutes = null;
    let = seconds = null;
    let = millis = null;

    if(min < 10){
        minutes = "0"+min+":";
    }else{
        minutes = ""+min+":";
    }

    if(sec < 10){
        seconds = "0"+sec+":";
    }else{
        seconds = ""+sec+":";
    }

    millis = ""+ms;

    return minutes+seconds+millis;
}


let timer = new Timer(setText,display_results, 100);

function start_button_click() {
    //timer.start();
    timer.start_run()
}

function stop_button_click() {
    // timer.stop();
    timer.stop_run();
}

function reset_button_click(){
    timer.reset();
}

