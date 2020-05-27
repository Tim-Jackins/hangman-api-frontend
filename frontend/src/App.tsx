import React from "react"
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  useRouteMatch,
  useParams,
} from "react-router-dom"
import {
  Nav,
  Navbar,
  Jumbotron,
  Form,
  FormControl,
  Button,
  InputGroup,
} from "react-bootstrap"
import { UserForm } from "./UserForm"
import { Field } from "./Field"

const api_root = 'http://127.0.0.1:5000/'

type MyProps = {
  // using `interface` is also ok
  message: string
}
type MyState = {
  name: ""
  public_id: ""
  token: ""
  signed_in: false
}

export default class App extends React.Component<MyProps, MyState> {
  constructor(props: MyProps) {
    super(props)

    this.tryToSignUp = this.tryToSignUp.bind(this)
  }

  // componentDidMount() {
  // }

  // componentDidUpdate() {
  // }

  public tryToSignUp(form: HTMLFormElement) {
    // console.log("Trying to sign up.")
    // console.log(form.serializeArray())
    const data = new FormData(form)

    const body = {
      'username': data.get('username'),
      'password': data.get('password')
    }

    fetch(api_root + 'register/', {
      method: 'POST',
      body: body
    })
  }

  render() {
    // console.log('in parent')
    // console.log(this.tryToSignUp)
    // this.tryToSignUp()
    return (
      <Router>
        <Navbar bg="light" expand="lg">
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="mr-auto">
              <Nav.Link href="/">Home</Nav.Link>
              <Nav.Link href="/sign_up">Sign up</Nav.Link>
              <Nav.Link href="/topics">Topics</Nav.Link>
            </Nav>
            <Form inline>
              <InputGroup>
                <FormControl placeholder="Username" aria-label="Username" />
                <InputGroup.Append>
                  <Button variant="outline-success">Login</Button>
                </InputGroup.Append>
              </InputGroup>
            </Form>
          </Navbar.Collapse>
        </Navbar>
        <div className="container">
          <Switch>
            <Route path="/sign_up">
            {/* <form>
                    <fieldset>
                        <legend>Choices</legend>

                        <input type="radio" name="choice" id="choice1" value="choice1" checked/>
                        <label htmlFor="choice1">Choice 1</label>

                        <input type="radio" name="choice" id="choice2" value="choice2"/>
                        <label htmlFor="choice2">Choice 2</label>
                    </fieldset>
                    <button type="submit">Do The Thing!</button>
            </form> */}

              {/* <SignUp onFinish={this.tryToSignUp} /> */}
              <UserForm
                action="http://localhost:4351/api/contactus"
                onFinish={ this.tryToSignUp }
                body={() => (
                  <React.Fragment>
                    <Jumbotron className="text-center mt-3">
                      <h1>Sign Up</h1>
                    </Jumbotron>
                    <Field id="username" label="Username" editor="textbox" />
                    <Field id="password" label="Password" editor="password" />
                    {/* <Field
            id="reason"
            label="Reason"
            editor="dropdown"
            options={["", "Marketing", "Support", "Feedback", "Jobs"]}
          />
          <Field id="notes" label="Notes" editor="multilinetextbox" /> */}
                  </React.Fragment>
                )}
              />
            </Route>
            <Route path="/topics">
              <Topics />
            </Route>
            <Route path="/">
              <Home />
            </Route>
          </Switch>
        </div>
      </Router>
    )
  }
}

function Home() {
  return <h1>Home</h1>
}

// function SignUp(FProps: any) {
//   console.log("inside first function")
//   console.log(FProps.onFinish)
//   return (
//     <UserForm
//       action="http://localhost:4351/api/contactus"
//       onFinish={FProps.onFinish}
//       body={() => (
//         <React.Fragment>
//           <Jumbotron className="text-center mt-3">
//             <h1>Sign Up</h1>
//           </Jumbotron>
//           <Field id="username" label="Username" editor="textbox" />
//           <Field id="password" label="Password" editor="password" />
//           {/* <Field
//             id="reason"
//             label="Reason"
//             editor="dropdown"
//             options={["", "Marketing", "Support", "Feedback", "Jobs"]}
//           />
//           <Field id="notes" label="Notes" editor="multilinetextbox" /> */}
//         </React.Fragment>
//       )}
//     />
//   )
// }

function Topics() {
  let match = useRouteMatch()

  return (
    <div>
      <h2>Topics</h2>

      <ul>
        <li>
          <Link to={`${match.url}/components`}>Components</Link>
        </li>
        <li>
          <Link to={`${match.url}/props-v-state`}>Props v. State</Link>
        </li>
      </ul>

      <Switch>
        <Route path={`${match.path}/:topicId`}>
          <Topic />
        </Route>
        <Route path={match.path}>
          <h3>Please select a topic.</h3>
        </Route>
      </Switch>
    </div>
  )
}

function Topic() {
  let { topicId } = useParams()
  return <h3>Requested topic ID: {topicId}</h3>
}
