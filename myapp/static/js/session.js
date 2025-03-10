export async function fetchSessionData(){
    try{
        const respose =await fetch('/session-data');
        const data = await respose.json();

        // keyにerrorが入ってなかったら 'data'をそのままreturn
        if(!data.error){
            return data
        }
        else{
            console.log(data.error);
            windows.location.href="/login";
        }
    }catch(error){
        console.error('Error fetching session data:',error)
    }
}

export function displaySessiondata(data){
    document.getElementById('username').innerText=data.username;
    document.getElementById('email').innerHTML=data.username;
    


}