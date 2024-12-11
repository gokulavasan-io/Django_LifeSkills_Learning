from django.contrib.auth.models import Group,Permission

def create_groups_permission(sender,**kwargs):
    
    try:
            #creating groups
        readers_group,created=Group.objects.get_or_create(name="Readers")
        authors_group,created=Group.objects.get_or_create(name="Authors")
        editors_group,created=Group.objects.get_or_create(name="Editors")
        
        #creating permissions
        
        readers_permission=[
            Permission.objects.get(codename="view_post")
        ]
        
        authors_permission=[
            Permission.objects.get(codename="add_post"),
            Permission.objects.get(codename="change_post"),
            Permission.objects.get(codename="delete_post"),
        ]
        can_publish, _ = Permission.objects.get_or_create(
            codename="can_publish",
            content_type_id=7,
            name="Can Publish Post"
        )
        editors_permission=[
            can_publish,
            Permission.objects.get(codename="add_post"),
            Permission.objects.get(codename="change_post"),
            Permission.objects.get(codename="delete_post"),
        ]
        
        # assigning Permissions 
        
        readers_group.permissions.set(readers_permission)
        authors_group.permissions.set(authors_permission)
        editors_group.permissions.set(editors_permission)
    except Exception as e:
        print(f"An error occured : {e}")
        
    
    print("Groups and Permissions added successfully")