
/*
    TimerOutput takes the amount of milliseconds in its constructor and converts it into 
    a String "mm:ss.ms"
*/
class TimerOutput {
    constructor(milliseconds) {
        this.milliseconds_total = milliseconds;
        this.ms = 0;
        this.sec = 0;
        this.min = 0;
        this.hour = 0;
        this.initializeFields();
    }

    initializeFields() {
        const min_factor = 60 * 1000;
        const hour_factor = min_factor * 60;

        this.hour = Math.floor(this.milliseconds_total / hour_factor)
        let ms_left = this.milliseconds_total - (this.hour  * hour_factor)
        this.min = Math.floor(this.milliseconds_total / min_factor);
        ms_left = ms_left - (this.min * min_factor)
        this.sec = Math.floor(ms_left / 1000);
        this.ms = ms_left - (this.sec * 1000);
        this.ms = Math.floor(this.ms / 100);
    }
    // get the string representaion of the milliseconds
    toString() {
        let hours = null;
        let minutes = null;
        let seconds = null;
        let millis = null;

        if(this.hour < 10){
            hours = "0" + this.hour + ":";
        }else{
            hours = ""+ this.hour + ":";
        }

        if (this.min < 10) {
            minutes = "0" + this.min + ":";
        } else {
            minutes = "" + this.min + ":";
        }

        if (this.sec < 10) {
            seconds = "0" + this.sec + ":";
        } else {
            seconds = "" + this.sec + ":";
        }

        millis = "" + this.ms;

        return hours + minutes + seconds + millis;
    }
}

class Timer {

    /*
    @parameter : output_id
        The id of an HTML-Element that will be used for output of the progresss

    @parameter : _results_id
        The id of an HTML-Element that will be used for posting the resulted time
        when the stop() method is called on this object

    @paramter : interval
        The interval (in milliseconds) in which the HTML-Element with the assigned output_id
        will be updated. 
    */
    constructor(output_id, _results_id, interval) {
        this.interval = interval;
        this.start_time = 0;
        this.repeat = null;
        this.counter = 0;
        this.stop_time = 0;
        this.pause_time = 0;
        this.pauseTotal = 0;
        this.isPaused = false;
        this.started = false;
        this.results_id = _results_id;
        this.output_id = output_id;
        this.time_elapsed = 0;
        this.run = null;
    }

    start() {
        if (this.started == false) {
            this.started = true;
            this.start_time = Date.now();
            this.repeat = setInterval(this.displayProgress, this.interval, this);
        }


        if (this.isPaused) {
            this.isPaused = false;

            // Calculate the difference between the pause time and this moment
            let difference = Date.now() - this.pause_time;

            // Add pauseTotal to the difference
            this.pauseTotal += difference;

            this.repeat = setInterval(this.displayProgress, this.interval, this);
        }
    }


    pause() {
        this.isPaused = true;
        this.pause_time = Date.now();
        clearInterval(this.repeat);
    }

    stop() {
        this.started = false;

        this.stop_time = Date.now() - this.start_time;
        let out = new TimerOutput(this.stop_time - this.pauseTotal);

        document.getElementById(this.results_id).value = out.toString();
        clearInterval(this.repeat);
    }

    reset() {
        this.start_time = Date.now();
        this.displayProgress(this);
    }

    /* 
        Update the value of the HTML-Element by element_id, that was passed to the constructor
        NOTE! The setInterval() function will create a new Instance of the Timer and run it in 
        a separate Thread. This is the reason for the @parameter:callerInstance. 
    
        @parameter : callerInstance
            Instance of the Timer calling this method. It enables access to the properties of the
            Timer object that is calling this method.
    
            In the start() method it is passed as a parameter to the displayProgress method via 
            setInterval function like so:
                this.repeat = setInterval(this.displayProgress, this.interval, this);
            As you can see setInterval takes three parameters here. The first two parameters are 
            mandatory. The first one takes the name of method to be called. The second one takes
            the interval in which that method should be called. And if you add more parameters 
            they will be passed to that method. 
    */
    displayProgress(callerInstance) {
        let ms_elapsed = Date.now() - callerInstance.start_time - callerInstance.pauseTotal;


        let out = new TimerOutput(ms_elapsed);
        document.getElementById(callerInstance.output_id).value = out.toString();
    }
}




