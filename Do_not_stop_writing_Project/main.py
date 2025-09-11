from flask import Flask, render_template_string

app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template_string("""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Welcome</title>
                    <style>
                        body, h1, h2 {
                            font-family: Arial, sans-serif;
                        text-align: center;
                            }
                        button {
                        padding: 10px 20px;
                        background-color: #FFFFFF;
                        border: 2px solid #FF3333;
                        color: #FF3333;
                        border-radius: 20px;
                        cursor: pointer;
                        font-size: 16px;
                        
                            }
                    button:hover {
                        background-color: #FF3333;
                        color: #FFFFFF;
                                }
                    </style>      
                </head>
                <body>
                    <h1>The Most <span style="color: #FF3333;">Dangerous</span> Writing App</h1>
                    <h2>Don’t stop writing, or all progress will be lost!</h2>
                    <div>
                        <a href="/write"><button>Start Writing</button></a>
                     </div>
                </body>
                </html
                """)


@app.route('/write')
def write():
    return render_template_string("""
            <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Welcome</title>
                    <style>
                        body {
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            height: 100vh;
                            background-color: white;
                            font-family: Arial, sans-serif;
                            margin: 0;
                            flex-direction: column;
                                }
                        .text-container {
                                width: 100%;
                                text-align: center;
                                display: flex;
                                justify-content: center;
                                align-items: flex-start;
                                position: relative;
                                margin-top: 20px;
                                            }
                        .text-box {
                            min-width: 200px;
                            max-width: 595px;
                            width: auto;
                            outline: none;
                            padding: 20px;
                            font-size: 18px;
                            line-height: 1.5;
                            word-wrap: break-word;
                            background-color: transparent;
                            color: black;
                            position: relative;
                            text-align: left;
                            white-space: normal;
                                             }
                        .text-box:empty:before {
                                content: "Start writing here...";
                                color: #D3D3D3;
                                font-style: italic;
                                position: absolute;
                                top: 20px; 
                                left: 20px;
                                pointer-events: none;
                                white-space: nowrap;
                                             }
                                             
                        #word_count {
                                width: 100%;
                                text-align: center;
                                margin-top: auto; 
                                margin-bottom: 20px; 
                                }
                                
                        #popup {
                            display: none;
                            text-align: center;
                            padding: 20px;
                            background-color: #f0f0f0;
                            border: 1px solid #ccc;
                            border-radius: 5px;
                            margin-top: 20px;
                            font-size: 18px;
                            position: fixed;
                            top: 50%;
                            left: 50%;
                            transform: translate(-50%, -50%);
                            z-index: 1001;
                                    }   
                                    
                        #popup button {
                                margin-top: 10px;
                                padding: 10px 20px;
                                font-size: 16px;
                                cursor: pointer;
                                         }  
                                         
                        #overlay {
                                display: none;
                                position: fixed;
                                top: 0;
                                left: 0;
                                width: 100%;
                                height: 100%;
                                background-color: rgba(0, 0, 0, 0.5);
                                z-index: 1000;
                                pointer-events: all;
                                    }

                                
                    </style>
                    <body>
                         <div id="overlay"></div>
                        <div class="text-container">
                            <div class="text-box" contenteditable="true" id="textinput" spellcheck="false" 
                                                                                            autofocus></div>
                        </div>
                        
                        <div id="word_count">Words Typed: 0</div>
                        
                        <div id="popup">
                            <p id="popup_message">You typed: 0 words</p>
                            <button onclick="resetText()">Type Again</button>
                        </div> 
    
                        <script>
                            let timer;
                            let blur_timer;
                            let blur_lvl = 0;
                            const text_input = document.getElementById("textinput");
                            const blur_delay = 2000;
                            const blur_step = 1000;
                            const max_blur = 3;
                            const word_count_div = document.getElementById("word_count");
                            const popup = document.getElementById("popup");
                            const popup_message = document.getElementById("popup_message");
                            const overlay = document.getElementById("overlay");
                            
                            function text_clear(){
                                    const word_count = count_words(text_input.innerText);
                                    show_popup(word_count);
                                    text_input.innerHTML = "";
                                    text_input.style.filter = "none";
                                    blur_lvl = 0;
                                    refresh_word_count();
                                    } 
                                    
                            function show_popup(word_count) {
                                popup_message.textContent = `You typed: ${word_count} words`;
                                popup.style.display = "block"; 
                                overlay.style.display = "block";
                                text_input.setAttribute('contenteditable', 'false');
                                         } 
                    
                            function hide_popup() {
                                popup.style.display = "none";
                                overlay.style.display = "none";
                                text_input.setAttribute('contenteditable', 'true');
                                        } 
                                    
                            function blur_text(){
                                blur_timer = setInterval(function(){
                                    if (blur_lvl < max_blur) {
                                        blur_lvl++;
                                        text_input.style.filter = `blur(${blur_lvl}px)`;
                                        }
                                    else {
                                        clearInterval(blur_timer);
                                        text_clear();
                                        }
                                        }, blur_step);
                                        }
                                        
                            function inactivity(){
                                clearTimeout(timer);
                                timer = setTimeout(function(){
                                    blur_text();
                                    }, blur_delay);
                                    }
                                    
                            function count_words(text) {
                                    const words = text.trim().split(/\s+/).filter(function(word) {
                                            return word.length > 0;
                                    });
                                    return words.length;
                                    }
                                    
                            function refresh_word_count() {
                                    const word_count = count_words(text_input.innerText);
                                    word_count_div.textContent = `Word Typed: ${word_count}`; 
                                    }    
                                    
                            function resetText() {
                                    text_input.innerHTML = "";
                                    text_input.setAttribute('contenteditable', 'true');
                                    text_input.focus();
                                    hide_popup();
                                    refresh_word_count();
                                            }
                                    
                            text_input.addEventListener("input", function(){
                                clearTimeout(timer);
                                clearInterval(blur_timer);
                                blur_lvl = 0;
                                text_input.style.filter = "none";
                                inactivity();
                                refresh_word_count();
                                }); 
                        </script>                    
                    </body>
                    </html>
         """)


if __name__ == '__main__':
    app.run(debug=True)
