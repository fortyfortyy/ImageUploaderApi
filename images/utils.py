def image_upload_path(instance, filename):
    # 'instance' is the instance of the Image model, and 'filename' is the original name of the uploaded file.
    return f"{instance.user.id}/images/{instance.id}/{filename}"
