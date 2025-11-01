import {Modal, Result, Button} from "antd";


function ResultModal({isOpen, onClose, isOk, title, subtitle}) {
    return (
        <Modal open={isOpen} onCancel={onClose} footer={<Button variant={'outlined'} color={'cyan'} onClick={onClose}>Закрыть</Button>}>
            {isOk ? (<Result status={"success"} title={title} subTitle={subtitle} />) :
                <Result status={"error"} title={title} subTitle={subtitle}/>}

        </Modal>
    )
}

export default ResultModal