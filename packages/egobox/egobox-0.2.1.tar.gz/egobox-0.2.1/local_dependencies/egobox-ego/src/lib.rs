//! This library implements Efficient Global Optimization method,
//! it is a port of [SMT EGO algorithm](https://smt.readthedocs.io/en/latest/_src_docs/applications/ego.html)
//!
//! The optimizer is able to deal with inequality constraints.
//! Objective and contraints are expected to computed grouped at the same time
//! hence the given function should return a vector where the first component
//! is the objective value and the remaining ones constraints values intended
//! to be negative in the end.   
//! The optimizer comes with a set of options to:
//! * specify the initial doe,
//! * parameterize internal optimization,
//! * parameterize mixture of experts,
//! * save intermediate results and allow hot restart,
//!
//! Example:
//!
//! ```no_run
//! # use ndarray::{array, Array2, ArrayView2};
//! # use egobox_ego::Egor;
//!
//! fn xsinx(x: &ArrayView2<f64>) -> Array2<f64> {
//!     (x - 3.5) * ((x - 3.5) / std::f64::consts::PI).mapv(|v| v.sin())
//! }
//!
//! // We ask for 10 evaluations of the objective function to get the result
//! let res = Egor::new(xsinx, &array![[0.0, 25.0]])
//!             .n_eval(10)
//!             .minimize()
//!             .expect("xsinx minimized");
//! println!("Minimum found f(x) = {:?} at x = {:?}", res.x_opt, res.y_opt);
//! ```
//!
//! The implementation relies on [Mixture of Experts](egobox_moe).
//! While [Egor] optimizer works with continuous data (i.e floats), the class [MixintEgor]
//! allows to make basic mixed-integer optimization by decorating `Egor` class.    
//!
//! Reference:
//!
//! * Bartoli, Nathalie, et al. [Adaptive modeling strategy for constrained global
//! optimization with application to aerodynamic wing design](https://www.sciencedirect.com/science/article/pii/S1270963818306011)
//!  Aerospace Science and technology 90 (2019): 85-102.
//!
//!
mod egor;
mod errors;
mod mixint;
mod mixintegor;
mod sort_axis;
mod types;
mod utils;

pub use crate::egor::*;
pub use crate::errors::*;
pub use crate::mixint::*;
pub use crate::mixintegor::*;
pub use crate::types::*;
