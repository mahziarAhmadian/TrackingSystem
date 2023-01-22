class SystemPermissions:

    def all_permissions(self):
        system_permissions = {

            'TypePermissions': ['AddType', 'EditType', 'DeleteType'],

            'UserPermissions': ['EditUser', 'GetUserDetail', 'DeleteUser'],

            'ProjectPermissions': ['AddProject', 'EditProject', 'DeleteProject', 'GetProject', 'GetProjectDocuments',
                                   'DeleteProjectDocument'],

            'ModulePermissions': ['AddModule', 'EditModule', 'DeleteModule', 'GetModule'],

            'MetePermissions': ['AddMeter', 'GetMeter', 'EditMeter', 'DeleteMeter'],

            'TruckPermissions': ['AddTruck', 'GetTruck', 'EditTruck', 'DeleteTruck'],

            'TruckRecordsPermissions': ['AddTruckRecord', 'GetTruckRecord', 'DeleteTruckRecord', 'EditTruckRecord'],

            'MeterSitePermissions': ['AddMeterSite', 'GetMeterSite', 'DeleteMeterSite', 'EditMeterSite'],

            'TruckMeterSite': ['AddTruckMeterSite', 'GetTruckMeterSite', 'DeleteTruckMeterSite'],

            'Counter': ['CountAllData'],

            'MeterTypePermissions': ['AddMeterType', 'GetMeterType'],

        }
        return system_permissions
