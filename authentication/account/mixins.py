from django.shortcuts import redirect

class LogoutRequiredMixins(object):
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        
        return super(LogoutRequiredMixins, self).dispatch(*args, **kwargs)