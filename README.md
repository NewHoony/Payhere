# Payhere Project
![main](https://user-images.githubusercontent.com/105026915/230719007-434700a7-95c5-4bf0-85ed-4d967a532055.png)

## 개발 환경
● Ubuntu 22.04 <br>
● Django 3.2.8 <br>
● MySQL  5.7 <br>

## [ Comment ]
  § 기존 로컬 PC의 Mysql 버전이 8.0.31이라 ubuntu 환경에서 새로 5.7버전 DB를 생성해 진행하였습니다 <br><br>
  § Mysql 5.7에 따른 장고 버전이 요구되어 3.2.8 버전으로 다운그레이드하여 진행하였습니다 <br><br>
  § 함수형 views를 사용하였으며 forms.py를 통해 html 페이지에서 쉽게 랜더링 할 수 있도록 설정하였습니다 <br><br>
  § {% if user.is_authenticated %} 사용하여 인증된 유저만 가계부에 접근 할 수 있도록 하였습니다 <br><br>
  § JWT 토큰을 활용한 유저 인증 부분은 <b>Chat GPT</b>를 활용하여 개발 하였으며 최대한 구현 해보도록 하였지만 부족한 부분이 많습니다. <br><br>
  § 가계부 부분에서 tinyurl를 통해 url 생성은 완료 하였지만 역량 부족으로 인한 일정 시간 후 만료 구현은 하지 못하였습니다. <br><br>

## Database
  ▶ PayhereDB 생성 후 payhere라는 유저를 새로 생성하고 권한을 부여하여 DB 접근의 보안을 높혔습니다. <br>
  ▶ DB 구현 ( mysql 설치 → DB생성 → 유저 생성 → 권한 부여 → 마이그레이션 체크 ) <br>
  ![payhere(4)](https://user-images.githubusercontent.com/105026915/230716169-b2d618d6-460c-460d-9dfd-aaf57354df41.png)
  ![payhere(5)](https://user-images.githubusercontent.com/105026915/230716173-beebc327-5abe-4f7e-bee9-a190228581cc.png)
  ![payhere(7)](https://user-images.githubusercontent.com/105026915/230716176-235ff32c-9762-43f6-965e-49a58401ae08.png)
  ![payhere(8)](https://user-images.githubusercontent.com/105026915/230716182-df4d5f68-14a5-4094-af5e-e194d8a4deb3.png)
  ![payhere(10)](https://user-images.githubusercontent.com/105026915/230716191-b6e36572-ae92-42c0-8672-01ac58ee89cd.png)
  ![payhere(12)-migrate 확인](https://user-images.githubusercontent.com/105026915/230716192-afc47066-93ce-41a1-bc22-85c857f092e2.png)
  <hr>

## Acc App ( 유저 인증 앱 )
▶ 장고에서 제공하는 from django.contrib.auth.models import User를 통해 테이블을 사용하였습니다. <br>
▶ JWT 토큰을 처음 접해 Chat GPT를 활용하여 코드를 작성하였으며 serializers, API 부분은 계속해서 학습 중 입니다. <br>

<hr>
    
    @api_view(['POST'])
      def refresh_jwt_token(request):
         jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
         jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
         payload = jwt_payload_handler(request.user)
         token = jwt_encode_handler(payload)
      return Response({'token': token}, status=status.HTTP_200_OK)
☑️ refresh_jwt_token: 인증된 사용자에 대해 기존 JWT(JSON Web Token)를 갱신하기 위해 작성하였으며 만료 시 새 토큰을 생성할 수 있도록 하였습니다. <br>
☑️ jwt_payload_handler: 사용자 인스턴스가 주어진 JWT에 대한 페이로드를 생성합니다 <br>
☑️ jwt_encode_handler: 페이로드를 JWT로 인코딩합니다. <br>
☑️ payload: JWT의 페이로드가 포함되도록 하였습니다 jwt_payload_handler 객체를 호출하여 생성됩니다. <br>
☑️ token: 인코딩된 JWT가 포함된 문자열입니다. jwt_encode_handler를 호출하여 생성됩니다. <br>
☑️ Response: 뷰가 반환하는 HTTP 응답에 성공 시 HTTP 상태 코드를 포함하는 모듈인 status가 http_200_ok를 출력하도록 하였습니다. <br>

<hr>

    @api_view(['POST'])
    def token_view(request):
        email = request.data.get('email')
        password = request.data.get('password')

    user = authenticate(username=email, password=password)
    if user is not None:
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return Response({'token': token})
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
☑️ email과 password를 통해 토큰을 확인 할 수 있도록 하였습니다. <br>
☑️ authenticate에 성공하면 사용자에 대한 JWT를 생성하고 반환하고 성공하지 못하면 오류 응답을 반환하도록 하였습니다. 
        
<hr>

![5](https://user-images.githubusercontent.com/105026915/230714913-4d13b7cc-1358-4fb0-9f60-231b2959c65a.png)
![6](https://user-images.githubusercontent.com/105026915/230714916-89dd8b6b-1bb6-488f-b833-7e831f6d8a3c.png)









## Book ( 가계부 앱 )
▶ 테이블 생성 시 영수증 이미지를 같이 첨부 할 수 있도록 이미지 필드를 추가하였습니다<br> § auto_now_add를 추가해 현재 시간을 기준으로 입력되도록 설정하였습니다.

    class Book(models.Model):
      date = models.DateField(auto_now_add=True)
      memo = models.CharField(max_length=100)
      money = models.DecimalField(max_digits=10, decimal_places=0)
      receipt = models.ImageField(upload_to='receipts/', blank=True, null=True) 
![1](https://user-images.githubusercontent.com/105026915/230716781-d64d5b37-a1f7-4f3b-91bc-748ca15b61e7.png)
![2](https://user-images.githubusercontent.com/105026915/230716784-3e0a5958-b487-4072-8bb1-08593316371b.png)


▶ Detail 페이지의 url 구현<br> 

    def detail(request, pk):
      books= Book.objects.get(pk=pk)
      url = request.build_absolute_uri(reverse('book:detail', args=[books.pk]))
      s = pyshorteners.Shortener()
      short_url = s.tinyurl.short(url)
      return render(request, 'book/detail.html', {'books': books, 'short_url': short_url})
 
 ☑️ 함수의 결과를 인수로 전달하도록 build_absolute_uri의 메서드를 사용. 또한 URL을 생성하고 URL에 값을 전달하기 위해 사용하였습니다.<br>
 ☑️ 단축 url를 만들기 위해 s라는 변수를 만들어 pyshorteners.Shortener를 초기화 <br>
 ☑️ tinyurl를 활용하여 단축 url 생성 <br>
 ☑️ detail 접근 시 생성한 개채와 그 개체로 이동할 수 있는 단축 url 하이퍼 링크를 생성하였습니다.
 <hr>
 
    def duplicate(request, pk):
      books = Book.objects.get(pk=pk)
      books.pk = None
      books.date = timezone.now()
      books.save()
      return redirect('book:index')
   ☑️ 객체의 기본 키를 변수 books로 설정하고 None 값을 주어 생성 시 새로운 기본키를 가지도록 하였습니다.<br>
   ☑️ 생성 시간은 timezone.now()를 통해 복제한 당시 시간대로 설정하였습니다. <br>
