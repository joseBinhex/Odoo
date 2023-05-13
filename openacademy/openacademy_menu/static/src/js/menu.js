
odoo.define('openacademy_menu.openacademy_action', function (require) {
    "use strict";
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var KanbanRecord = require('web.KanbanRecord')
    KanbanRecord.include({
        /**
         * @override
         * @private
         *
         * 
         */

        _openRecord: function (element) {
            var self = this;
            var original_super = this._super;  // save reference to original _super 
            var $field = $(this);
            var id = $field.attr("id"); // extract data ID from field

            var context = {
                active_id: id,
            };

            self.getSession().user_has_group('openacademy_menu.openacademy_app_user').then(function(hasGroup) {
                if (hasGroup) {
                    self._rpc({
                        // Get view id
                        model:'ir.model.data',
                        method:'xmlid_to_res_model_res_id',
                        args: ['openacademy_menu.view_add_attendee_wizards'], // Kanban view id of res.users model
                    }).then(function(data){                
                        // Open view
                        self.do_action({
                            name: 'Join to Session',
                            type: 'ir.actions.act_window',
                            res_model: 'openacademy.joinses', // Module name
                            target: 'new', // new because we want a pop-up window
                            views: [[data[1], 'form']], // data[1] variable contains the view id
                            context: context, // Add the active_id to the context
                        });
                        
                    });
                } else if (self.getSession().user_has_group('openacademy_menu.openacademy_app_manager')) {
                    original_super.apply(self, [element]);  // original context
                }
            });
        },
    });
    
    var OpenAcademyAction = AbstractAction.extend({
        hasControlPanel: false,
        contentTemplate: "academy.buttons",
        events: {
            'click .o_openacademy_course_btn': '_onCourseBtnClick',
            'click .o_openacademy_session_btn': '_onSessionBtnClick',
            'click .o_openacademy_res_course_btn': '_onResponsibleBtnClick',
            'click .o_openacademy_oportunities_btn': '_onOportunitiesBtnClick',
            'click .o_openacademy_back': '_goBack',
        },
        
        start: function () {
            var self = this;  
            var def = this._super.apply(this, arguments);
            
            this._rpc({
                model: 'res.company',
                method: 'search_read',
                kwargs: {
                    fields: ['name', 'logo'],
                    limit: 1,
                },
            }).then(function (company) {
                self.context = _.extend(self.context || {}, {
                    res: {
                        company: company[0] || {},
                    },
                });

                // Update company name in the footerr
                var companyName = self.$('.o_company_name');
                if (companyName.length) {
                    companyName.text(self.context.res.company.name);
                }

                // Update company logo in the footer
                var companyLogo = self.$('.o_company_logo img');
                if (companyLogo.length && self.context.res.company.logo) {
                    companyLogo.attr('src', 'data:image/png;base64,' + self.context.res.company.logo);

                    
                }
            });
            return def;
        },
         // Using static url **pending to change
        _goBack: function() {
            location.href ='http://10.1.0.50/web#action=101&active_id=mail.box_inbox&cids=1&menu_id=83';
        },

        _onCourseBtnClick: function() {
            var self = this;
            self._rpc({
                // Get view id
                model:'ir.model.data',
                method:'xmlid_to_res_model_res_id',
                args: ['openacademy_menu.course_list_custom'], // Custom view id
            }).then(function(data){                
                // Open view
                self.do_action({
                    name: 'Courses',
                    type: 'ir.actions.act_window',
                    res_model: 'openacademy.course', // Module name
                    target: 'fullscreen',
                    views: [[data[1], 'list'], [false, 'form']], // data[1] variable contains the view id
                    context: {
                            'search_default_responsible_search': 1,
                            // hide create button
                            'create': false
                        },  
                 });
            });
          },
        
        _onSessionBtnClick: function() {
            var self = this;
            var contextt = {
                'create': false
            };
            self._rpc({
                // Get view id for the first view
                model: 'ir.model.data',
                method: 'xmlid_to_res_model_res_id',
                args: ['openacademy_menu.session_kanban_custom'], // Custom view id
            }).then(function(data){
                var view_id = data[1];
                // Get view id for the second view
                self._rpc({
                    model: 'ir.model.data',
                    method: 'xmlid_to_res_model_res_id',
                    args: ['openacademy.sessions_form'], // Custom view id
                }).then(function(data2){
                    // Open view
                    self.do_action({
                        name: 'Session',
                        type: 'ir.actions.act_window',
                        res_model: 'openacademy.sessions', // Module name
                        target: 'fullscreen',
                        views: [[view_id, 'kanban'], [data2[1], 'form']], // views in order: list, kanban, form
                        context: contextt,
                        res_id: self.id,
                    });
                });
            });
        },

        _onResponsibleBtnClick: function() {
            var self = this;
            var contextt = {
                'create': false
            };
            self._rpc({
                // Get view id
                model:'ir.model.data',
                method:'xmlid_to_res_model_res_id',
                args: ['res.users.kanban_view'], // Kanban view id of res.users model
            }).then(function(data){                
                // Open view
                self.do_action({
                    name: 'Responsibles of Courses',
                    type: 'ir.actions.act_window',
                    res_model: 'res.users', // Module name
                    target: 'fullscreen',
                    views: [[data[1], 'kanban'], [false, 'form']], // data[1] variable contains the view id
                    context: contextt
                });
                
            });
        },

        _onOportunitiesBtnClick: function() {
            var self = this;
            var contextt = {
                'create': false,
                'edit': false,
                'kanban_no_create': true,
            };
            self._rpc({
                // Get view id
                model:'ir.model.data',
                method:'xmlid_to_res_model_res_id',
                args: ['openacademy_menu.opportunities_kanban_custom'], // Kanban view id of res.users model
            }).then(function(data){                
                // Open view
                self.do_action({
                    name: 'Opportunities of Courses',
                    type: 'ir.actions.act_window',
                    res_model: 'crm.lead', // Module name
                    target: 'fullscreen',
                    domain: [['course_id', '!=', false]], // filter to get only courses with data
                    views: [[data[1], 'kanban'], [false, 'form']], // data[1] variable contains the view id
                    context: contextt
                });
                
            });
        },
        

    });

    core.action_registry.add('openacademy_menu.action', OpenAcademyAction);

    return OpenAcademyAction;
});
