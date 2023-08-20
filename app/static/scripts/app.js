var app_methods = {};

app_methods.change_panel = function(panel,admin_panel){
    this.search_bar_val = '',
    this.panel = panel,
    this.admin_panel = admin_panel
}


// User is searching with a specified uuid
app_methods.onClick_searchBarAdvs = function(){
    this.pages = null;
    if (this.search_bar_val != null){
        data = {'search_bar_val':this.search_bar_val};

        if (this.admin_panel == 'admin-users-info'){
            axios.post('/on-click-search-bar-user',data).then(response => {
                this.users_info = response.data
                for (let i = 0; i < this.users_info.length; i++) {
                    if (this.users_info[i][1] === null) {
                        this.users_info[i][1] = 'بدون نام کاربری';
                    }
                    if (this.users_info[i][2] !== null){
                        this.users_info[i][2] = "https://www.openstreetmap.org/#map=18/" + this.users_info[i][2]['latitude']+ "/" + this.users_info[i][2]['longitude']
                    }
                  }
            });
        }
        else {
            axios.post('/on-click-search-bar-request',data).then(response => {
                this.res_queue = this.res_done = this.res_processing = null
                if (response.data.length !== 0){
                    if (response.data[0][2] == '/add-two-numbers'){
                        this.change_panel('admin','admin-res-add-calc')
                        admin_panel = 'admin-res-add-calc'
                    }
                    else if (response.data[0][2] == '/hide-text-in-image'){
                        this.change_panel('admin','admin-res-steg-img')
                        admin_panel = 'admin-res-steg-img'
                    }
                    else if (response.data[0][2] == '/get-hidden-text-from-image'){
                        this.change_panel('admin','admin-res-extr-steg-img')
                        admin_panel = 'admin-res-extr-steg-img'
                    }
                    else if (response.data[0][2] == '/hide-text-in-sound'){
                        this.change_panel('admin','admin-res-steg-audio')
                        admin_panel = 'admin-res-steg-audio'
                    }
                    else if (response.data[0][2] == '/get-hidden-text-from-sound'){
                        this.change_panel('admin','admin-res-extr-audio')
                        admin_panel = 'admin-res-extr-audio'
                    }
                    if (response.data[0][5] == 'done'){
                        this.res_done = response.data
                    }
                    else if (response.data[0][5] == 'processing'){
                        this.res_processing = response.data
                    }
                    else {
                        this.res_queue = response.data
                    }
                }
            });
        }
        this.search_bar_val = null;      
    }}


app_methods.getUserReqs = function(user_id, username, add_calc_page, img_hide_page, img_get_page, sound_hide_page, sound_get_page){
    this.user_id = user_id;
    this.username = username;
    arr_res_done = [], arr_res_processing = [], arr_res_queue = []

    var data = { 'user_id' : user_id, 
                'page':{
                    'add_calc_page':add_calc_page,
                    'img_hide_page':img_hide_page,
                    'img_get_page':img_get_page,
                    'sound_hide_page':sound_hide_page,
                    'sound_get_page':sound_get_page
                }                
    }
    axios.post('/admin-get-user-reqs', data).then(response => { 

        for (let i = 0; i < response.data['result']['add_calc'][0].length; i++) {
            if (response.data['result']['add_calc'][0][i][5] === 'done'){
                arr_res_done.push(response.data['result']['add_calc'][0][i])
            }
            else if (response.data['result']['add_calc'][0][i][5] === 'processing'){
                arr_res_processing.push(response.data['result']['add_calc'][0][i])
            }
            else {
                arr_res_queue.push(response.data['result']['add_calc'][0][i])
            }
        }

        this.add_calc_completed_reqs = arr_res_done
        this.add_calc_processing_reqs = arr_res_processing
        this.add_calc_inQueue_reqs = arr_res_queue
        this.add_calc_pages = response.data['result']['add_calc'][1]
        arr_res_done = [], arr_res_processing = [], arr_res_queue = []
    

        for (let i = 0; i < response.data['result']['img_hide'][0].length; i++) {
            if (response.data['result']['img_hide'][0][i][5] === 'done'){
                arr_res_done.push(response.data['result']['img_hide'][0][i])
            }
            else if (response.data['result']['img_hide'][0][i][5] === 'processing'){
                arr_res_processing.push(response.data['result']['img_hide'][0][i])
            }
            else {
                arr_res_queue.push(response.data['result']['img_hide'][0][i])
            }
        }
        this.img_hide_completed_reqs = arr_res_done
        this.img_hide_processing_reqs = arr_res_processing
        this.img_hide_inQueue_reqs = arr_res_queue
        this.img_hide_pages = response.data['result']['img_hide'][1]
        arr_res_done = [], arr_res_processing = [], arr_res_queue = []

        for (let i = 0; i < response.data['result']['img_get'][0].length; i++) {
            if (response.data['result']['img_get'][0][i][5] === 'done'){
                arr_res_done.push(response.data['result']['img_get'][0][i])
            }
            else if (response.data['result']['img_get'][0][i][5] === 'processing'){
                arr_res_processing.push(response.data['result']['img_get'][0][i])
            }
            else {
                arr_res_queue.push(response.data['result']['img_get'][0][i])
            }
        }
        this.img_get_completed_reqs = arr_res_done
        this.img_get_processing_reqs = arr_res_processing
        this.img_get_inQueue_reqs = arr_res_queue
        this.img_get_pages = response.data['result']['img_get'][1]
        arr_res_done = [], arr_res_processing = [], arr_res_queue = []

        for (let i = 0; i < response.data['result']['sound_hide'][0].length; i++) {
            if (response.data['result']['sound_hide'][0][i][5] === 'done'){
                arr_res_done.push(response.data['result']['sound_hide'][0][i])
            }
            else if (response.data['result']['sound_hide'][0][i][5] === 'processing'){
                arr_res_processing.push(response.data['result']['sound_hide'][0][i])
            }
            else {
                arr_res_queue.push(response.data['result']['sound_hide'][0][i])
            }
        }
        this.sound_hide_completed_reqs = arr_res_done
        this.sound_hide_processing_reqs = arr_res_processing
        this.sound_hide_inQueue_reqs = arr_res_queue
        this.sound_hide_pages = response.data['result']['sound_hide'][1]
        arr_res_done = [], arr_res_processing = [], arr_res_queue = []

        for (let i = 0; i < response.data['result']['sound_get'][0].length; i++) {
            if (response.data['result']['sound_get'][0][i][5] === 'done'){
                arr_res_done.push(response.data['result']['sound_get'][0][i])
            }
            else if (response.data['result']['sound_get'][0][i][5] === 'processing'){
                arr_res_processing.push(response.data['result']['sound_get'][0][i])
            }
            else {
                arr_res_queue.push(response.data['result']['sound_get'][0][i])
            }
        }
        this.sound_get_completed_reqs = arr_res_done
        this.sound_get_processing_reqs = arr_res_processing
        this.sound_get_inQueue_reqs = arr_res_queue
        this.sound_get_pages = response.data['result']['sound_get'][1]
    })
    this.change_panel('admin','admin-user-reqs')
}

app_methods.admin_resRouteUsers = function(route,page,new_panel){
    data = {'route':route, 'page':page}
    this.activeIndexPage = page;
    this.change_panel('admin',new_panel);
    arr_res_done = [];
    arr_res_processing = [];
    arr_res_queue = [];
    axios.post('/admin-res-route-users',data).then(response => {    

        for (let i = 0; i < response.data['result'].length; i++) {
            if (response.data['result'][i][5] === 'done'){
                arr_res_done.push(response.data['result'][i])
            }
            else if (response.data['result'][i][5] === 'processing'){
                arr_res_processing.push(response.data['result'][i])
            }
            else {
                arr_res_queue.push(response.data['result'][i])
            }
        }
        this.res_done = arr_res_done
        this.res_processing = arr_res_processing
        this.res_queue = arr_res_queue
        
        this.pages = response.data['count_pages']
    })
};


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

app_methods.isActivePage = function(index){
    return index === this.activeIndexPage;
}

// check the active pages in user all reqs
app_methods.isActivePageAddCalc = function(index){ return index === this.activeIndexPageAddCalc; }
app_methods.isActivePageImgHide = function(index){ return index === this.activeIndexPageImgHide; }
app_methods.isActivePageImgGet = function(index){ return index === this.activeIndexPageImgGet; }
app_methods.isActivePageSoundHide = function(index){ return index === this.activeIndexPageSoundHide; }
app_methods.isActivePageSoundGet = function(index){ return index === this.activeIndexPageSoundGet; }


app_methods.changePageInUserReqsPanel = function(page, route){
    data = {'page':page , 'route':route , 'user_id':this.user_id}
    axios.post('/admin-user-res-route',data).then(response => {
        arr_res_done = []
        arr_res_processing = []
        arr_res_queue = []
        for (let i = 0; i < response.data['result'].length; i++) {
            
            if (response.data['result'][i][5] === 'done') {
                arr_res_done.push(response.data['result'][i])
            }
            else if (response.data['result'][i][5] === 'processing') {
                arr_res_processing.push(response.data['result'][i])
            }
            else {
                arr_res_queue.push(response.data['result'][i])
            }
        }

        if (route === '/add-two-numbers'){
            this.add_calc_completed_reqs = arr_res_done;
            this.add_calc_inQueue_reqs = arr_res_queue;
            this.add_calc_processing_reqs = arr_res_processing;
            this.activeIndexPageAddCalc = page;
        }
        else if (route === '/hide-text-in-image'){
            this.img_hide_completed_reqs = arr_res_done;
            this.img_hide_inQueue_reqs = arr_res_queue;
            this.img_hide_processing_reqs = arr_res_processing;
            this.activeIndexPageImgHide = page;
        }
        else if (route === '/get-hidden-text-from-image'){
            this.img_get_completed_reqs = arr_res_done;
            this.img_get_inQueue_reqs = arr_res_queue;
            this.img_get_processing_reqs = arr_res_processing;
            this.activeIndexPageImgGet = page;
        }
        else if (route === '/hide-text-in-sound'){
            this.sound_hide_completed_reqs = arr_res_done;
            this.sound_hide_inQueue_reqs = arr_res_queue;
            this.sound_hide_processing_reqs = arr_res_processing;
            this.activeIndexPageSoundHide = page;
        }
        else if (route === '/get-hidden-text-from-sound'){
            this.sound_get_completed_reqs = arr_res_done;
            this.sound_get_inQueue_reqs = arr_res_queue;
            this.sound_get_processing_reqs = arr_res_processing;
            this.activeIndexPageSoundGet = page;
        }
    })
}


// for all users
app_methods.admin_resUsersInfo = function(page,new_panel){
    data = {'page':page}
    this.activeIndexPage = page;
    this.change_panel('admin',new_panel);
    axios.post('/admin-users-info',data).then(response => {
        this.users_info = response.data["result"]
        for (let i = 0; i < this.users_info.length; i++) {
            if (this.users_info[i][1] === null) {
                this.users_info[i][1] = 'بدون نام کاربری';
            }
            if (this.users_info[i][2] !== null){
                this.users_info[i][2] = "https://www.openstreetmap.org/#map=18/" + this.users_info[i][2]['latitude']+ "/" + this.users_info[i][2]['longitude']
            }
        }
        this.pages = response.data['count_pages']
    })
    this.change_panel('admin','admin-users-info');
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
        user_id:'',

        // result for all pages
        res_done: [],
        res_processing : [],
        res_queue: [],

        // Dashboard info
        all_requests: 0,
        completed_requests: 0 ,
        processing_requests: 0 ,
        inQueue_requests : 0,
        all_add_requests: 0,
        all_audio_requests: 0,
        all_img_requests: 0,

        // User all requests 
        add_calc_processing_reqs:[],
        add_calc_inQueue_reqs:[],
        add_calc_completed_reqs:[],
        add_calc_pages:'',
        activeIndexPageAddCalc:1,

        img_hide_processing_reqs:[],
        img_hide_inQueue_reqs:[],
        img_hide_completed_reqs:[],
        img_hide_pages:'',
        activeIndexPageImgHide:1,

        img_get_processing_reqs:[],
        img_get_inQueue_reqs:[],
        img_get_completed_reqs:[],
        img_get_pages:'',
        activeIndexPageImgGet:1,

        sound_hide_processing_reqs:[],
        sound_hide_inQueue_reqs:[],
        sound_hide_completed_reqs:[],
        sound_hide_pages:'',
        activeIndexPageSoundHide:1,

        sound_get_processing_reqs:[],
        sound_get_inQueue_reqs:[],
        sound_get_completed_reqs:[],
        sound_get_pages:'',
        activeIndexPageSoundGet:1,
        // #END User all requests 

        // search-bar
        search_bar_val: null,

        // count of the current admin_panel pages for pagination
        pages: '',
        activeIndexPage: '',
    } },
    
    delimiters: ["${", "}$"],    
    methods:app_methods,
    
}).mount('#app')