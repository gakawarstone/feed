uvicorn app.main:app --host 0.0.0.0 --port 8000 &
rq worker -u redis://172.18.0.1 &

wait -n
exit $?
