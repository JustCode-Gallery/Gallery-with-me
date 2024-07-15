document.getElementById('univ-authenticate').addEventListener('click', function () {
    const email = document.getElementById('email').value;
    const university = document.getElementById('university').value;

    fetch('https://univcert.com/api/v1/certify', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'key':'07cda2ba-afdb-46a9-af15-0849a9b6bfd6', 'email': email, 'univName': university, 'univ_check':true })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('인증되었습니다.');
                // 인증 성공 시 버튼 텍스트 변경
                document.getElementById('send-verification-code').disabled = false;
                document.getElementById('univ-authenticate').disabled = true;
            } else {
                alert('인증에 실패했습니다.');
            }
        });
});