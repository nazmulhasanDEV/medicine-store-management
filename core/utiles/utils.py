from django.shortcuts import get_object_or_404, get_list_or_404

def get_single_object(model_class, pk):
    try:
        obj = get_object_or_404(model_class, pk=pk)
    except model_class.DoesNotExist:
        obj = None
    return obj

