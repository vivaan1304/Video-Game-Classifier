import { Button, Image,  FormControl, Input, Box, Spinner } from '@chakra-ui/react'
import './App.css'
import { useState } from 'react'
import { useForm } from 'react-hook-form'
import axios from 'axios';
import image from '/home/vivaan/Desktop/projects/Machine+DeepLearning/video-game-classifier/Video-Game-Classifier/backend/flask-app/templates/static/image.jpeg'
// export default function HookForm() {

  
// }
function App() {
  const {
    handleSubmit,
    register,
    formState: {isSubmitting }
  } = useForm();

  const [state, changeState] = useState(false)
  const [file, setFile] = useState(null)
  const [prediction, setPrediction] = useState(null)

  const onFormSubmit = async () => {
    changeState(!state);
    const form = new FormData();
    form.append("image", file);
    console.log(file)
    const res = await axios.post('http://127.0.0.1:8080/get_prediction', form, {headers: {"content-type":"multipart/form-data"}});
    console.log(res)
    setPrediction(res.data)
  }
  const onErrors = (errs) => console.log(errs)
    return (
    <div>
      {!state &&
    <form onSubmit={handleSubmit(onFormSubmit, onErrors)}>
        <FormControl isRequired>
         <Input placeholder='Input Image' size='lg' type='file' accept='image/*' required {...register('image')} onChange={(e) => setFile(e.target.files[0])}/>
      </FormControl>
      <Button mt={4} colorScheme='teal' isLoading={isSubmitting} type='submit'>
          Submit
        </Button>
      </form>
}
      {state && (prediction!=null && (<Box boxSize='sm'> <Image src={ image} alt='{prediction}' /><br/><p>{prediction}</p></Box>))}
      {state && (prediction==null && (<Spinner />))}

      </div>
    )
}

export default App;
