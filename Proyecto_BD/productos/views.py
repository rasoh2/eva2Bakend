from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from productos.models import Producto

# Vistas del CRUD protegidas por login_required (Etapa 3)

@login_required
def mostrarIndex(request):
    return render(request, 'index.html')

@login_required
def mostrarListado(request):
    productos = Producto.objects.all()
    return render(request, 'listado.html', {'productos': productos})

@login_required
def mostrarFormRegistrar(request):
    return render(request, 'form_registrar.html')

@login_required
def insertarProducto(request):
    if request.method == 'POST':
        nom = request.POST.get('txtnom')
        mar = request.POST.get('cbomar')
        pre = request.POST.get('txtpre')
        pro = Producto(nombre=nom, marca=mar, precio=pre)
        pro.save()
        datos = {'msjOk': 'Registro grabado exitosamente'}
        return render(request, 'form_registrar.html', datos)
    else:
        datos = {'msjErr': 'La solicitud no se puede procesar !!'}
        return render(request, 'form_registrar.html', datos)

@login_required
def mostrarFormActualizar(request, id):
    pro = get_object_or_404(Producto, id=id)
    return render(request, 'form_actualizar.html', {'producto': pro})

@login_required
def actualizarProducto(request, id):
    if request.method == 'POST':
        pro = get_object_or_404(Producto, id=id)
        pro.nombre = request.POST.get('txtnom')
        pro.marca = request.POST.get('cbomar')
        pro.precio = request.POST.get('txtpre')
        pro.save()
        return redirect('listado')
    return redirect('listado')

@login_required
def eliminarProducto(request, id):
    pro = get_object_or_404(Producto, id=id)
    pro.delete()
    return redirect('listado')