<?php
// Игнорируем отмену загрузки страницы пользователем
ignore_user_abort();

// Говорим что время на выполнение скрипта не ограничено
set_time_limit(1);

// Говорим что соединение надо закрыть
header('Connection: close');

// Перенаправляем если нужно
//header('Location: http://site.com');

// Отчищаем все буферы вывода 
@ob_end_flush();
@ob_flush();
@flush();

// Заканчиваем сессию пользователя (именно сессия и не давала 
// запускать выполнение ещё одного скрипта для этого пользователя 
// т.к. запуск скриптов лочится на файл сессий)
if(session_id()){
    session_write_close();
}

echo exec('whoami'); 
//$old_path = getcwd();
//chdir('/home/sysop/pi_weather/data/web/');
$output=shell_exec('sudo /home/sysop/pi_weather/data/web/restartw.sh');
echo $output; 
//chdir($old_path);

?>
