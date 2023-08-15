var app_methods = {};

app_methods.change_panel = function(panel,admin_panel){

    //  SignIn Info
    this.username= '',
    this.password= '',

    this.panel = panel;
    this.admin_panel = admin_panel
}


app_methods.getUserReqs = function(user_id){
    var data = { 'user_id' : user_id }
    axios.post('/admin-get-user-reqs', data).then(response => { 
        console.log(response.data) 
        if (response.data['status-code'] == 200) { 
            this.add_calc_completed_reqs = response.data["result"]["add_calc"]["done"]
            this.add_calc_processing_reqs = response.data["result"]["add_calc"]["processing"]
            this.add_calc_inQueue_reqs = response.data["result"]["add_calc"]["in queue"]
            
            this.img_hide_completed_reqs = response.data["result"]["img_hide"]["done"] 
            this.img_hide_processing_reqs = response.data["result"]["img_hide"]["processing"]
            this.img_hide_inQueue_reqs = response.data["result"]["img_hide"]["in queue"]

            this.img_get_completed_reqs = response.data["result"]["img_get"]["done"] 
            this.img_get_processing_reqs = response.data["result"]["img_get"]["processing"]
            this.img_get_inQueue_reqs = response.data["result"]["img_get"]["in queue"]   

            this.sound_hide_completed_reqs = response.data["result"]["sound_hide"]["done"]
            this.sound_hide_processing_reqs = response.data["result"]["sound_hide"]["processing"]
            this.sound_hide_inQueue_reqs = response.data["result"]["sound_hide"]["in queue"]

            this.sound_get_completed_reqs = response.data["result"]["sound_get"]["done"]
            this.sound_get_processing_reqs = response.data["result"]["sound_get"]["processing"]
            this.sound_get_inQueue_reqs = response.data["result"]["sound_get"]["in queue"]
        }})
        this.change_panel('admin','admin-user-reqs')
}



// Get admin dashboard info
app_methods.getAdminDashboardInfo = function(){
    var data = {
        'username':this.username,
        'password':this.password,
    }
    axios.post('/signin', data).then(response => {  
        if (response.data['status-code'] == 200) { 
            this.processing_requests = response.data["result"]["processing"]  // count of processing
            this.inQueue_requests = response.data["result"]["in queue"]     // count of queue
            this.completed_requests = response.data["result"]["done"]   // count of done
            this.all_requests = response.data["result"]["done"] + response.data["result"]["in queue"] + response.data["result"]["processing"]
            
            this.all_add_requests = response.data["result"]["all_add_reqs"]
            this.all_audio_requests = response.data["result"]["all_audio_steg_reqs"]
            this.all_img_requests = response.data["result"]["all_img_steg_reqs"]
            this.change_panel('admin','admin-dashboard')
        }})
};


app_methods.admin_resAddCalc = function(){
    axios.post('/admin-res-add-calc').then(response => {          
        this.res_queue = response.data["result"]["queue"]
        this.res_processing = response.data["result"]["processing"]
        this.res_done = response.data["result"]["done"]  
    })
    this.change_panel('admin','admin-res-add-calc');
};

app_methods.admin_resStegImg = function(){
    axios.post('/admin-res-steg-img').then(response => {          
        this.res_queue = response.data["result"]["queue"]
        this.res_processing = response.data["result"]["processing"]
        this.res_done = response.data["result"]["done"]  
    })
    this.change_panel('admin','admin-res-steg-img');
};

app_methods.admin_resExtrStegImg = function(){
    axios.post('/admin-res-extr-steg-img').then(response => {          
        this.res_queue = response.data["result"]["queue"]
        this.res_processing = response.data["result"]["processing"]
        this.res_done = response.data["result"]["done"]  
    })
    this.change_panel('admin','admin-res-extr-steg-img');
};

app_methods.admin_resStegAudio = function(){
    axios.post('/admin-res-steg-audio').then(response => {          
        this.res_queue = response.data["result"]["queue"]
        this.res_processing = response.data["result"]["processing"]
        this.res_done = response.data["result"]["done"]  
    })
    this.change_panel('admin','admin-res-steg-audio');
};

app_methods.admin_resExtrStegAudio = function(){
    axios.post('/admin-res-extr-audio').then(response => {          
        this.res_queue = response.data["result"]["queue"]
        this.res_processing = response.data["result"]["processing"]
        this.res_done = response.data["result"]["done"]  
    })
    this.change_panel('admin','admin-res-extr-audio');
};

// for all users
app_methods.admin_usersInfo = function(){
    axios.post('/admin-users-info').then(response => {
        this.users_info = response.data["result"]
        console.log(this.users_info)
        for (let i = 0; i < this.users_info.length; i++) {
            if (this.users_info[i][1] === null) {
                this.users_info[i][1] = 'بدون نام کاربری';
            }
          }
    })
    this.change_panel('admin','admin-users-info');
};



// Signin
app_methods.signIn = function(){
    if (this.username =='admin' && this.password == 'admin'){
        this.getAdminDashboardInfo();
        return;
    }
    else { Swal.fire({title:'خطا' ,text:'نام کاربری یا رمز عبور اشتباه است', icon:'error', confirmButtonText:'تایید'}) }
};


Vue.createApp({

    data(){ return {        
        panel: 'sign-in',
        admin_panel: '',

        // admin
        users_info:'' ,

        //  SignIn Info
        username: '',
        password: '',

        // result for all pages
        res_done: '',
        res_processing : '',
        res_queue: '',

        // Dashboard info
        all_requests: 0,
        completed_requests: 0 ,
        processing_requests: 0 ,
        inQueue_requests : 0,
        all_add_requests: 0,
        all_audio_requests: 0,
        all_img_requests: 0,

        // User all requests 
        add_calc_processing_reqs:'',
        add_calc_inQueue_reqs:'',
        add_calc_completed_reqs:'',

        img_hide_processing_reqs:'',
        img_hide_inQueue_reqs:'',
        img_hide_completed_reqs:'',

        img_get_processing_reqs:'',
        img_get_inQueue_reqs:'',
        img_get_completed_reqs:'',

        sound_hide_processing_reqs:'',
        sound_hide_inQueue_reqs:'',
        sound_hide_completed_reqs:'',

        sound_get_processing_reqs:'',
        sound_get_inQueue_reqs:'',
        sound_get_completed_reqs:'',
        // #END User all requests 

    } },
    
    delimiters: ["${", "}$"],    
    methods:app_methods,
    
}).mount('#app')