from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from cupons.forms import CuponApllyForm
from cupons.models import Cupon


@require_POST
def cupon_aplly(request):
    now = timezone.now()
    form = CuponApllyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            cupon = Cupon.objects.get(
                code__iexact=code,
                valid_from__lte=now,
                valid_to__gte=now,
                active=True,
            )
            request.session['cupon_id'] = cupon.id
        except Cupon.DoesNotExist:
            request.session['cupon_id'] = None
    return redirect('cart:cart_detail')
