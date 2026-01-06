import {Modal} from "antd";
import {Viewer, Worker, SpecialZoomLevel} from "@react-pdf-viewer/core";

function ModalPreview({isModalOpen, onClose, mDocId, groupDocId, fileName}) {
    let apiUrl = import.meta.env.VITE_SCANNER_API_URL;
    if (apiUrl === undefined) {
        apiUrl = 'http://localhost:3000'
        console.error("No scanner url were found")
    }
    const pdfUrl = `${apiUrl}/documents/file?mdoc_id=${mDocId}&group_doc_id=${groupDocId}&filename=${fileName}`;

    return (
        <>
            <Modal open={isModalOpen} onCancel={onClose}
                   width={{
                xs: '50%',
                sm: '50%',
                md: '50%',
                lg: '50%',
                xl: '50%',
                xxl: '60%',
            }}
                footer={null}
                   style={{top: 20}} // Moves the modal closer to the top of the screen
                   bodyStyle={{height: '1400px', width: "1000px", overflowX: 'auto', overflowY: 'auto'}}>
                <Worker workerUrl="https://unpkg.com/pdfjs-dist@3.4.120/build/pdf.worker.min.js">
                    <Viewer defaultScale={SpecialZoomLevel.PageFit}
                            fileUrl={pdfUrl}/>
                </Worker>
            </Modal>
        </>
    )
}


export default ModalPreview