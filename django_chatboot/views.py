from django.shortcuts import render
from django.http import JsonResponse
import openai
import os


open_api_key = os.environ.get('OPENAI_key')
openai.api_key = open_api_key


def ask_openai(question):
    response = openai.Completion.create(
        model = "text-davinci-003",
        prompt = question,
        max_tokens = 150,
        n = 1,
        stop = None,
        temperature = 0.7,
    )
    print(response)
    answer = response.choices[0].text.lstrip()
    return answer

def chatboot(request):
    if request.method == 'POST':
        message = request.POST.get('message') 
        response = ask_openai(message)
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatboot.html')
