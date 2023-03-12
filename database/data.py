user_data = [
    {
        'username': 'admin',
        'password': '$2b$12$q0OSa5wwpo1xkUfRCx2DZuPqWt04CQ.CNR.lV6oGqnpVmww2055Py',
        'real_name': '李立伟',
        'gender': '1',
        'is_status': '1',
        'is_admin': '1'
    },
    {
        'username': '10001',
        'password': '$2b$12$q0OSa5wwpo1xkUfRCx2DZuPqWt04CQ.CNR.lV6oGqnpVmww2055Py',
        'real_name': '周淑芬',
        'gender': '2',
        'is_status': '1',
        'is_admin': '0'
    },
    {
        'username': '2021230522',
        'password': '$2b$12$q0OSa5wwpo1xkUfRCx2DZuPqWt04CQ.CNR.lV6oGqnpVmww2055Py',
        'real_name': '王橓西',
        'gender': '1',
        'is_status': '1',
        'is_admin': '0'
    }
]

role_data = [
    {'role_name': '管理员', 'role_code': 'admin', 'is_status': '1', 'description': '管理员拥有所有权限'},
    {'role_name': '教师', 'role_code': 'teacher', 'is_status': '1', 'description': '教师可以管理学生'},
    {'role_name': '学生', 'role_code': 'student', 'is_status': '1', 'description': '学生可以查看自己的信息'}
]

menu_data = [
    {
        'parent_id': 0, 'menu_title': '仪表盘', 'menu_type': '1', 'router_name': 'dashboard', 'sub_count': 0,
        'router_path': '/dashboard', 'component': 'dashboard/index.vue', 'sort': 1, 'icon': 'index',
        'permission': '*', 'is_show': '1', 'is_sub': '0'
    },
    {
        'parent_id': 0, 'menu_title': '课程管理', 'menu_type': '1', 'router_name': 'course', 'sub_count': 2,
        'router_path': '/course', 'component': '', 'sort': 2, 'icon': 'index',
        'permission': '', 'is_show': '1', 'is_sub': '1'
    },
    {
        'parent_id': 2, 'menu_title': '我的课程', 'menu_type': '2', 'router_name': 'my-course', 'sub_count': 0,
        'router_path': '/course/me', 'component': 'course/me/index.vue', 'sort': 3, 'icon': 'index',
        'permission': 'course:me:list', 'is_show': '1', 'is_sub': '0'
    },
    {
        'parent_id': 2, 'menu_title': '所有课程', 'menu_type': '2', 'router_name': 'all-course', 'sub_count': 0,
        'router_path': '/course/all', 'component': 'course/all/index.vue', 'sort': 4, 'icon': 'index',
        'permission': 'course:all:list', 'is_show': '1', 'is_sub': '0'
    },
    {
        'parent_id': 0, 'menu_title': '考勤管理', 'menu_type': '1', 'router_name': 'attendance', 'sub_count': 2,
        'router_path': '/attendance', 'component': '', 'sort': 5, 'icon': 'index',
        'permission': '', 'is_show': '1', 'is_sub': '1'
    },
    {
        'parent_id': 5, 'menu_title': '发布签到', 'menu_type': '2', 'router_name': 'publish', 'sub_count': 0,
        'router_path': '/attendance/publish', 'component': 'attendance/publish/index.vue', 'sort': 6, 'icon': 'index',
        'permission': 'attendance:publish:list', 'is_show': '1', 'is_sub': '0'
    },
    {
        'parent_id': 5, 'menu_title': '签到记录', 'menu_type': '2', 'router_name': 'record', 'sub_count': 0,
        'router_path': '/attendance/record', 'component': 'attendance/record/index.vue', 'sort': 7, 'icon': 'index',
        'permission': 'attendance:record:list', 'is_show': '1', 'is_sub': '0'
    },
    {
        'parent_id': 0, 'menu_title': '校园管理', 'menu_type': '1', 'router_name': 'attendance', 'sub_count': 3,
        'router_path': '/attendance', 'component': '', 'sort': 8, 'icon': 'index',
        'permission': '', 'is_show': '1', 'is_sub': '1'
    },
    {
        'parent_id': 5, 'menu_title': '班级管理', 'menu_type': '2', 'router_name': 'publish', 'sub_count': 0,
        'router_path': '/school/classes', 'component': 'school/classes/index.vue', 'sort': 9, 'icon': 'index',
        'permission': 'school:classes:list', 'is_show': '1', 'is_sub': '0'
    },
    {
        'parent_id': 5, 'menu_title': '专业管理', 'menu_type': '2', 'router_name': 'major', 'sub_count': 0,
        'router_path': '/school/major', 'component': 'school/major/index.vue', 'sort': 10, 'icon': 'index',
        'permission': 'school:major:list', 'is_show': '1', 'is_sub': '0'
    },
    {
        'parent_id': 5, 'menu_title': '学院管理', 'menu_type': '2', 'router_name': 'college', 'sub_count': 0,
        'router_path': '/school/college', 'component': 'school/college/index.vue', 'sort': 11, 'icon': 'index',
        'permission': 'school:college:list', 'is_show': '1', 'is_sub': '0'
    },
    {
        'parent_id': 0, 'menu_title': '系统管理', 'menu_type': '1', 'router_name': 'system', 'sub_count': 3,
        'router_path': '/system', 'component': '', 'sort': 12, 'icon': 'index',
        'permission': '', 'is_show': '1', 'is_sub': '1'
    },
    {
        'parent_id': 12, 'menu_title': '用户管理', 'menu_type': '2', 'router_name': 'user', 'sub_count': 0,
        'router_path': '/system/user', 'component': 'system/user/index.vue', 'sort': 13, 'icon': 'index',
        'permission': 'system:user:list', 'is_show': '1', 'is_sub': '0'
    },
    {
        'parent_id': 12, 'menu_title': '角色管理', 'menu_type': '2', 'router_name': 'role', 'sub_count': 0,
        'router_path': '/system/role', 'component': 'system/role/index.vue', 'sort': 14, 'icon': 'index',
        'permission': 'system:role:list', 'is_show': '1', 'is_sub': '0'
    },
    {
        'parent_id': 12, 'menu_title': '菜单管理', 'menu_type': '2', 'router_name': 'menu', 'sub_count': 0,
        'router_path': '/system/menu', 'component': 'system/menu/index.vue', 'sort': 15, 'icon': 'index',
        'permission': 'system:menu:list', 'is_show': '1', 'is_sub': '0'
    },
    {
        'parent_id': 0, 'menu_title': '关于系统', 'menu_type': '1', 'router_name': 'about', 'sub_count': 0,
        'router_path': '/about', 'component': '', 'sort': 16, 'icon': 'index',
        'permission': '', 'is_show': '1', 'is_sub': '0'
    }
]

user_role_data = [
    {'user_id': 1, 'role_id': 1},
    {'user_id': 2, 'role_id': 2},
    {'user_id': 3, 'role_id': 3}
]

role_menu_data = [
    {'role_id': 1, 'menu_id': 1},
    {'role_id': 1, 'menu_id': 2},
    {'role_id': 1, 'menu_id': 3},
    {'role_id': 1, 'menu_id': 4},
    {'role_id': 1, 'menu_id': 5},
    {'role_id': 1, 'menu_id': 6},
    {'role_id': 1, 'menu_id': 7},
    {'role_id': 1, 'menu_id': 8},
    {'role_id': 1, 'menu_id': 9},
    {'role_id': 1, 'menu_id': 10},
    {'role_id': 1, 'menu_id': 11},
    {'role_id': 1, 'menu_id': 12},
    {'role_id': 1, 'menu_id': 13},
    {'role_id': 1, 'menu_id': 14},
    {'role_id': 1, 'menu_id': 15},
    {'role_id': 1, 'menu_id': 16},
    {'role_id': 2, 'menu_id': 1},
    {'role_id': 2, 'menu_id': 2},
    {'role_id': 2, 'menu_id': 3},
    {'role_id': 2, 'menu_id': 4},
    {'role_id': 2, 'menu_id': 5},
    {'role_id': 2, 'menu_id': 6},
    {'role_id': 2, 'menu_id': 7},
    {'role_id': 2, 'menu_id': 8},
    {'role_id': 2, 'menu_id': 9},
    {'role_id': 2, 'menu_id': 10},
    {'role_id': 2, 'menu_id': 11},
    {'role_id': 2, 'menu_id': 16},
    {'role_id': 3, 'menu_id': 1},
    {'role_id': 3, 'menu_id': 2},
    {'role_id': 3, 'menu_id': 3},
    {'role_id': 3, 'menu_id': 16},
]

college_data = [
    {'college_name': '信息与通信工程'},
    {'college_name': '控制科学与工程'},
    {'college_name': '计算机科学与技术'},
]

major_data = [
    {'major_name': '通信与信息系统', 'college_id': 1},
    {'major_name': '信号与信息处理', 'college_id': 1},
    {'major_name': '控制理论与控制工程', 'college_id': 2},
    {'major_name': '系统工程', 'college_id': 2},
    {'major_name': '检测技术与自动化装置', 'college_id': 2},
    {'major_name': '计算机系统结构', 'college_id': 3},
    {'major_name': '计算机应用技术', 'college_id': 3},
    {'major_name': '物联网工程', 'college_id': 1}
]

classes_data = [
    {'classes_name': '通信与信息系统-1班', 'major_id': 1},
    {'classes_name': '通信与信息系统-2班', 'major_id': 1},
    {'classes_name': '信号与信息处理-1班', 'major_id': 2},
    {'classes_name': '信号与信息处理-2班', 'major_id': 2},
    {'classes_name': '控制理论与控制工程-1班', 'major_id': 3},
    {'classes_name': '控制理论与控制工程-2班', 'major_id': 3},
    {'classes_name': '控制理论与控制工程-3班', 'major_id': 3},
    {'classes_name': '系统工程-高级班', 'major_id': 4},
    {'classes_name': '检测技术与自动化装置-初级班', 'major_id': 5},
    {'classes_name': '检测技术与自动化装置-进阶班', 'major_id': 5},
    {'classes_name': '计算机系统结构-初级班', 'major_id': 6},
    {'classes_name': '计算机系统结构-进阶班', 'major_id': 6},
    {'classes_name': '计算机应用技术-1班', 'major_id': 7},
    {'classes_name': '计算机应用技术-2班', 'major_id': 7},
    {'classes_name': '物联网工程-1班', 'major_id': 8},
    {'classes_name': '物联网工程-2班', 'major_id': 8},
    {'classes_name': '物联网工程-3班', 'major_id': 8},
    {'classes_name': '物联网工程-1班(专升本)', 'major_id': 8},
    {'classes_name': '物联网工程-2班(专升本)', 'major_id': 8}
]

student_classes_data = [
    {'user_id': 3, 'classes_id': 11}
]
